import pytest
import json
import os
import importlib
import pprint
import json
import logging
from django.shortcuts import reverse
from rest_framework.status import HTTP_200_OK

from baserow_vocabai_plugin.cloudlanguagetools import clt_interface, quotas
import cloudlanguagetools.languages

logger = logging.getLogger(__name__)


# tests which need to be run with CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES=no

def use_clt_real_services():
    os.environ['CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES'] = 'no'
    importlib.reload(cloudlanguagetools.servicemanager)
    clt_interface.reload_manager()    

@pytest.mark.django_db
def test_pinyin(api_client, data_fixture):
    use_clt_real_services()

    # CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES=no pytest baserow_vocabai_plugin/cloudlanguagetools/test_clt.py -k test_pinyin -s -rPP --log-cli-level=DEBUG
    # CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES=no pytest baserow_vocabai_plugin/cloudlanguagetools/test_clt.py -k test_pinyin
    assert os.environ['CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES'] == 'no'

    logger.info(f'starting test_pinyin')
    user, token = data_fixture.create_user_and_token()

    # update language data first
    # clt_interface.update_language_data()

    # create database and table
    # =========================
    
    logger.info(f'creating database and table')

    database = data_fixture.create_database_application(user=user)

    url = reverse("api:database:tables:async_create", kwargs={"database_id": database.id})
    response = api_client.post(url, {"name": "test_table_1"}, format="json", HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_200_OK
    json_response = response.json()
    table_id = json_response['id']

    # add chinese field
    # =================
    # cloudlanguagetools.languages.Language.zh_cn

    logger.info(f'adding chinese language field')

    response = api_client.post(
        reverse("api:database:fields:list", kwargs={"table_id": table_id}),
        {"name": "chinese", "type": "language_text", "language": cloudlanguagetools.languages.Language.zh_cn.name},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    pprint.pprint(response_json)
    chinese_field_id = response_json['id']
    assert response.status_code == HTTP_200_OK    

    # add pinyin field
    # ================

    logger.info(f'adding pinyin field')

    response = api_client.post(
        reverse("api:database:fields:list", kwargs={"table_id": table_id}),
        {
            "name": "pinyin", 
            "type": "chinese_romanization", 
            "transformation": "pinyin",
            "source_field_id": chinese_field_id, 
            'tone_numbers': False,
            'spaces': False,
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    pprint.pprint(response_json)
    assert response.status_code == HTTP_200_OK
    pinyin_field_id = response_json['id']

    # enter some data in the chinese field
    # ====================================

    logger.info(f'writing data to row')

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": table_id}),
        {f"field_{chinese_field_id}": "了"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_row = response.json()
    print('response_row after writing some data:')
    # pprint.pprint(response_row) 
    table_row_id = response_row['id']
    assert response.status_code == HTTP_200_OK

    # retrieve the row
    # ================

    logger.info('retrieving row')
    response = api_client.get(
        reverse("api:database:rows:item", kwargs={"table_id": table_id, 'row_id': table_row_id}),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_row = response.json()
    assert response.status_code == HTTP_200_OK
    pprint.pprint(response_row) 

    expected_output = {
        'format_revision': 1,
        'rendered_solution': 'le',
        'solution_overrides': [0],
        'solutions': [['le', 'liǎo', 'liào']]
    }

    assert response_row[f'field_{pinyin_field_id}'] == expected_output


    # modify the pinyin field
    # =======================

    logger.info('updating row, the pinyin field')
    field_value = {
        'format_revision': 1,
        'rendered_solution': 'le',
        'solution_overrides': [1],
        'solutions': [['le', 'liǎo', 'liào']]
    }
    response = api_client.patch(
        reverse("api:database:rows:item", kwargs={"table_id": table_id, 'row_id': table_row_id}),
        {f"field_{pinyin_field_id}": field_value},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_row = response.json()
    logger.info(pprint.pformat(response_row))
    assert response.status_code == HTTP_200_OK


    expected_output = {
        'format_revision': 1,
        'rendered_solution': 'liǎo',
        'solution_overrides': [1],
        'solutions': [['le', 'liǎo', 'liào']]
    }
    assert response_row[f'field_{pinyin_field_id}'] == expected_output

    # retrieve the row again, make sure the id on the pinyin field is correct
    # =======================================================================

    logger.info('retrieving row')
    response = api_client.get(
        reverse("api:database:rows:item", kwargs={"table_id": table_id, 'row_id': table_row_id}),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_row = response.json()
    assert response.status_code == HTTP_200_OK
    # pprint.pprint(response_row) 

    expected_field_value = {
        'format_revision': 1,
        'rendered_solution': 'liǎo',
        'solution_overrides': [1],
        'solutions': [['le', 'liǎo', 'liào']]
    }

    assert response_row[f'field_{pinyin_field_id}'] == expected_field_value

    # modify pinyin derived field, use tone numbers
    # =============================================

    logger.info(f'modifying pinyin field to use tone numbers')

    response = api_client.patch(
        # reverse("api:database:fields:item", kwargs={"id": pinyin_field_id,"table_id": table_id}),
        f'/api/database/fields/{pinyin_field_id}/',
        {
            "name": "pinyin", 
            "type": "chinese_romanization", 
            "transformation": "pinyin",
            "source_field_id": chinese_field_id, 
            'tone_numbers': True,
            'spaces': False,
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    # logger.debug(f'after switching to tone numbers: {pprint.pformat(response_json)}')
    assert response.status_code == HTTP_200_OK

    # retrieve row again, we should see tone numbers in the pinyin field
    # ==================================================================

    logger.info('retrieving row to make sure the pinyin field now has tone numbers')
    response = api_client.get(
        reverse("api:database:rows:item", kwargs={"table_id": table_id, 'row_id': table_row_id}),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_row = response.json()
    assert response.status_code == HTTP_200_OK
    logger.debug(f'response after switching to tone numbers: {pprint.pformat(response_row)}')
    
    expected_output = {
        'format_revision': 1,
        'rendered_solution': 'le5',
        'solution_overrides': [0],
        'solutions': [['le5', 'liao3', 'liao4']]
    }    
    assert response_row[f'field_{pinyin_field_id}'] == expected_output

    # change chinese text, make sure pinyin gets updated
    # ==================================================

    new_chinese = '没有'
    logger.info(f'changing chinese field to {new_chinese}')

    response = api_client.patch(
        reverse("api:database:rows:item", kwargs={"table_id": table_id, 'row_id': table_row_id}),
        {f"field_{chinese_field_id}": new_chinese},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_row = response.json()
    assert response.status_code == HTTP_200_OK
    pprint.pprint(response_row)

    expected_pinyin = {
        'format_revision': 1,
        'rendered_solution': 'mei2you3',
        'solution_overrides': [0],
        'solutions': [['mei2you3']]
    }
    assert response_row[f'field_{pinyin_field_id}'] == expected_pinyin