from baserow.config.celery import app

from baserow.contrib.database.table.models import Table
from baserow.contrib.database.rows.signals import before_rows_update, rows_updated
from baserow.contrib.database.table.signals import table_updated

from . import instance as clt_instance

import time

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
def run_clt_translation_all_rows(self, table_id, source_language, target_language, service, source_field_id, target_field_id):
    for row_id_list in iterate_row_id_buckets(table_id):
        logger.info(f'scheduling translation for bucket of {len(row_id_list)} rows')
        run_clt_translation_many_rows.delay(source_language, target_language, service, table_id, row_id_list, source_field_id, target_field_id)

@app.task(
    bind=True,
    soft_time_limit=EXPORT_SOFT_TIME_LIMIT,
    time_limit=EXPORT_TIME_LIMIT,
)
def run_clt_translation_many_rows(self, source_language, target_language, service, table_id, row_id_list, source_field_id, target_field_id):
    logger.info(f'run_clt_translation_many_rows table_id: {table_id} row count: {len(row_id_list)}')

    for row in process_row_id_bucket_iterate_rows(table_id, row_id_list):
        text = getattr(row, source_field_id)
        if text != None and len(text) > 0:
            # logger.info(f'getting translation for row {row}, text: {text}')
            translated_text = clt_instance.get_translation(text, source_language, target_language, service)
            setattr(row, target_field_id, translated_text)
            # logger.info(f'updated row: {row}')
            row.save()



# transliteration
# ================

# noinspection PyUnusedLocal
@app.task(
    bind=True,
    soft_time_limit=EXPORT_SOFT_TIME_LIMIT,
    time_limit=EXPORT_TIME_LIMIT,
)
def run_clt_transliteration_all_rows(self, table_id, transliteration_id, source_field_id, target_field_id):
    for row_id_list in iterate_row_id_buckets(table_id):
        logger.info(f'scheduling transliteration for bucket of {len(row_id_list)} rows')
        run_clt_transliteration_many_rows.delay(transliteration_id, table_id, row_id_list, source_field_id, target_field_id)

@app.task(
    bind=True,
    soft_time_limit=EXPORT_SOFT_TIME_LIMIT,
    time_limit=EXPORT_TIME_LIMIT,
)
def run_clt_transliteration_many_rows(self, transliteration_id, table_id, row_id_list, source_field_id, target_field_id):
    logger.info(f'run_clt_transliteration_many_rows table_id: {table_id} row count: {len(row_id_list)} field_id: {target_field_id}')

    for row in process_row_id_bucket_iterate_rows(table_id, row_id_list):
        text = getattr(row, source_field_id)
        if text != None and len(text) > 0:
            # logger.info(f'getting transliteration for row {row}, text: {text}')
            result = clt_instance.get_transliteration(text, transliteration_id)
            setattr(row, target_field_id, result)
            # logger.info(f'updated row: {row}')
            row.save()    


# dictionary lookup
# =================

# noinspection PyUnusedLocal
@app.task(
    bind=True,
    soft_time_limit=EXPORT_SOFT_TIME_LIMIT,
    time_limit=EXPORT_TIME_LIMIT,
)
def run_clt_lookup_all_rows(self, table_id, lookup_id, source_field_id, target_field_id):
    for row_id_list in iterate_row_id_buckets(table_id):
        logger.info(f'scheduling lookup for bucket of {len(row_id_list)} rows')
        run_clt_lookup_many_rows.delay(lookup_id, table_id, row_id_list, source_field_id, target_field_id)


@app.task(
    bind=True,
    soft_time_limit=EXPORT_SOFT_TIME_LIMIT,
    time_limit=EXPORT_TIME_LIMIT,
)
def run_clt_lookup_many_rows(self, lookup_id, table_id, row_id_list, source_field_id, target_field_id):
    logger.info(f'run_clt_lookup_many_rows table_id: {table_id} row count: {len(row_id_list)} field_id: {target_field_id}')

    for row in process_row_id_bucket_iterate_rows(table_id, row_id_list):
        text = getattr(row, source_field_id)
        if text != None and len(text) > 0:
            # logger.info(f'getting lookup for row {row}, text: {text}')
            result = clt_instance.get_dictionary_lookup(text, lookup_id)
            setattr(row, target_field_id, result)
            # logger.info(f'updated row: {row}')
            row.save()