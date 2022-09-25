from baserow.config.celery import app

from baserow.contrib.database.table.models import Table
from baserow.contrib.database.rows.signals import before_rows_update, rows_updated
from baserow.contrib.database.table.signals import table_updated

from django.conf import settings
import redis
import json

from . import clt_interface
from .quotas import QuotaOverUsage

import os
import time
import requests
import pprint

import logging
logger = logging.getLogger(__name__)

EXPORT_SOFT_TIME_LIMIT = 60 * 60
EXPORT_TIME_LIMIT = EXPORT_SOFT_TIME_LIMIT + 60


TASK_ITERATION_SIZE_PLAN = [
    [5, 1],
    [5, 2],
    [5, 10],
    [5, 100],
    [5, 500],
    [5, 2000],
    [5, 200000]
]

def iterate_row_id_buckets(table_id):
    step_size_array = []
    for entry in TASK_ITERATION_SIZE_PLAN:
        count = entry[0]
        step_size = entry[1]
        for i in range(0, count):
            step_size_array.append(step_size)

    # first, collect all row IDs
    base_queryset = Table.objects
    table = base_queryset.select_related("database__group").get(id=table_id)
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/
    table_model = table.get_model()
    row_id_list = []
    for row in table_model.objects.all():
        row_id = row.id
        row_id_list.append(row_id)    

    while len(row_id_list) > 0:
        iteration_size = step_size_array[0]
        step_size_array = step_size_array[1:]
        iteration_row_id_list = row_id_list[0:iteration_size]
        row_id_list = row_id_list[iteration_size:]
        yield iteration_row_id_list


def process_row_id_bucket_iterate_rows(table_id, row_id_list):

    base_queryset = Table.objects
    table = base_queryset.select_related("database__group").get(id=table_id)
    # logger.info(f'table: {table}')

    table_model = table.get_model()

    row_list = []
    for row_id in row_id_list:
        row = table_model.objects.get(id=row_id)
        row_list.append(row)

    size_cutoff = 50

    if len(row_list) < size_cutoff:
        before_return = before_rows_update.send(
            None,
            rows=row_list,
            user=None,
            table=table,
            model=table_model,
            updated_field_ids=None,
        )

    for row in row_list:
        yield row

    if len(row_list) < size_cutoff:
        rows_updated.send(
            None,
            rows=row_list,
            user=None,
            table=table,
            model=table_model,
            before_return=before_return,
            updated_field_ids=None
        )
    else:
        # refresh whole table
        table_updated.send(None, table=table, user=None, force_table_refresh=True)


# translation 
# ===========

# noinspection PyUnusedLocal
@app.task(
    bind=True,
    soft_time_limit=EXPORT_SOFT_TIME_LIMIT,
    time_limit=EXPORT_TIME_LIMIT,
)
def run_clt_translation_all_rows(self, table_id, source_language, target_language, service, source_field_id, target_field_id, usage_user_id):
    # populating all rows is still a single celery task, but we break it up so that we can notify the user
    # about work in progress

    try:
        for row_id_list in iterate_row_id_buckets(table_id):
            for row in process_row_id_bucket_iterate_rows(table_id, row_id_list):
                text = getattr(row, source_field_id)
                if text != None and len(text) > 0:
                    translated_text = clt_interface.get_translation(text, source_language, target_language, service, usage_user_id)
                    setattr(row, target_field_id, translated_text)
                    row.save()
    except QuotaOverUsage:
        logger.exception(f'could not complete translation for user {usage_user_id}')



# transliteration
# ================

# noinspection PyUnusedLocal
@app.task(
    bind=True,
    soft_time_limit=EXPORT_SOFT_TIME_LIMIT,
    time_limit=EXPORT_TIME_LIMIT,
)
def run_clt_transliteration_all_rows(self, table_id, transliteration_id, source_field_id, target_field_id, usage_user_id):
    try:
        for row_id_list in iterate_row_id_buckets(table_id):
            for row in process_row_id_bucket_iterate_rows(table_id, row_id_list):
                text = getattr(row, source_field_id)
                if text != None and len(text) > 0:
                    result = clt_interface.get_transliteration(text, transliteration_id, usage_user_id)
                    setattr(row, target_field_id, result)
                    row.save()
    except QuotaOverUsage:
        logger.exception(f'could not complete transliteration for user {usage_user_id}')

# dictionary lookup
# =================

# noinspection PyUnusedLocal
@app.task(
    bind=True,
    soft_time_limit=EXPORT_SOFT_TIME_LIMIT,
    time_limit=EXPORT_TIME_LIMIT,
)
def run_clt_lookup_all_rows(self, table_id, lookup_id, source_field_id, target_field_id, usage_user_id):
    try:
        for row_id_list in iterate_row_id_buckets(table_id):
            for row in process_row_id_bucket_iterate_rows(table_id, row_id_list):
                text = getattr(row, source_field_id)
                if text != None and len(text) > 0:
                    result = clt_interface.get_dictionary_lookup(text, lookup_id, usage_user_id)
                    setattr(row, target_field_id, result)
                    row.save()        
    except QuotaOverUsage:
        logger.exception(f'could not complete dictionary lookup for user {usage_user_id}')



# retrieving language data
# ========================

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    logger.info('setup_periodic_tasks')
    
    # run every 30s (debug only)
    # period = 30
    period = 3600 * 3
    sender.add_periodic_task(period, refresh_cloudlanguagetools_language_data.s(), name='cloudlanguagetools language data')
    
    # run once at startup
    refresh_cloudlanguagetools_language_data.delay()

    collect_user_data.delay()


# we want to auto-retry on requests.exceptions.ReadTimeout
@app.task(autoretry_for=(requests.exceptions.ReadTimeout,), retry_kwargs={'max_retries': 5}, queue='cloudlanguagetools')
def refresh_cloudlanguagetools_language_data():
    logger.info('refresh_cloudlanguagetools_language_data')
    clt_interface.update_language_data()


# collecting user data
# ====================

from django.contrib.auth import get_user_model
User = get_user_model()

from ..fields.vocabai_models import VocabAiUsage, USAGE_PERIOD_MONTHLY, USAGE_PERIOD_DAILY
from baserow.core.models import GroupUser
from baserow.contrib.database.models import Database
from baserow.contrib.database.table.models import Table

@app.task(queue='export')
def collect_user_data():
    logger.info('collect_user_data')

    base_url = os.environ['BASEROW_USER_STATS_URL']
    token = os.environ['BASEROW_USER_STATS_TOKEN']

    user_list = User.objects.all()

    user_record_list = []

    for user in user_list:
        # user model: https://docs.djangoproject.com/en/4.1/ref/contrib/auth/
        username = user.username
        last_login = user.last_login.isoformat()
        date_joined = user.date_joined.strftime('%Y-%m-%d')
        logger.info(f'user: {user} username: {user.username}')

        # lookup usage records
        usage_list = VocabAiUsage.objects.filter(user=user)
        for usage in usage_list:
            logger.info(f'usage: {usage} characters: {usage.characters} period: {usage.period} period_time: {usage.period_time}')

        # collect number of groups, tables, rows
        # need to locate GroupUser instances
        group_user_list = GroupUser.objects.filter(user=user)
        group_count = 0
        database_count = 0
        table_count = 0
        row_count = 0
        for group_user in group_user_list:
            logger.info(f'group_user: {group_user} group: {group_user.group}')
            group_count += 1
            # find all the databases in that group
            database_list = Database.objects.filter(group=group_user.group)
            for database in database_list:
                logger.info(f'database: {database}')
                database_count += 1
                # find all of the tables in that database
                table_list = Table.objects.filter(database=database)
                for table in table_list:
                    table_count += 1
                    row_count += table.get_model(field_ids=[]).objects.count()

        logger.info(f'user stats: last_login: {last_login} databases: {database_count} tables: {table_count} rows: {row_count}')
        logger.info(f'BASEROW_USER_STATS_URL: {base_url}')

        user_record_list.append({
            'username': username,
            'last_login': last_login,
            'date_joined': date_joined,
            'table_count': table_count,
            'row_count': row_count
        })
    
    # upload to baserow
    # =================

    # retrieve records first
    response = requests.get(
        f"{base_url}/?user_field_names=true",
        headers={
            "Authorization": f"Token {token}"
        }
    )    
    
    records = response.json()['results']
    baserow_username_to_id_map = {}
    for record in records:
        baserow_username_to_id_map[record['username']] = record['id']


    # determine which records need to be inserted or updated
    record_updates = []
    record_inserts = []
    for user_record in user_record_list:
        username = user_record['username']
        if username in baserow_username_to_id_map:
            # update
            update_record = user_record
            update_record['id'] = baserow_username_to_id_map[username]
            record_updates.append(update_record)
        else:
            # insert
            record_inserts.append(user_record)
    
    # do inserts
    if len(record_inserts) > 0:
        pprint.pprint(record_inserts)
        response = requests.post(
            f"{base_url}/batch/?user_field_names=true",
            headers={
                "Authorization": f"Token {token}",
                "Content-Type": "application/json"
            },
            json={
                "items": record_inserts
            }
        )    
        if response.status_code != 200:
            logger.error(response.content)

    # do updates
    if len(record_updates) > 0:
        pprint.pprint(record_updates)
        response = requests.patch(
            f"{base_url}/batch/?user_field_names=true",
            headers={
                "Authorization": f"Token {token}",
                "Content-Type": "application/json"
            },
            json={
                "items": record_updates
            }
        )    
        if response.status_code != 200:
            logger.error(response.content)    


    #pprint.pprint(records)





    

