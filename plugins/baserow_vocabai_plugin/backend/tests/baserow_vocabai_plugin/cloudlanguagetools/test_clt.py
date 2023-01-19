import pytest
import json
import os
import pprint
import json
from django.shortcuts import reverse
from rest_framework.status import HTTP_200_OK

from baserow_vocabai_plugin.cloudlanguagetools import clt_interface, quotas
import cloudlanguagetools.languages

# tests need to be run with CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES=yes


@pytest.mark.django_db
def test_language_data(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()

    # update language data first
    clt_interface.update_language_data()

    # make sure language list is available
    response = api_client.get(
        reverse("api:baserow_vocabai_plugin:language-list"),
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK

    # verify some things
    language_list = response.data
    assert 'fr' in language_list
    assert language_list['fr'] == 'French'


@pytest.mark.django_db
def test_quotas(api_client, data_fixture):
    assert os.environ['CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES'] == 'yes'

    user, token = data_fixture.create_user_and_token()

    # update language data first
    clt_interface.update_language_data()

    # verify initial usage record
    usage_record = quotas.get_usage_record(user.id)
    assert usage_record.monthly_usage_record.characters == 0
    assert usage_record.daily_usage_record.characters == 0
    
    # transformations on free and premium services should be allowed
    translation_result_str = clt_interface.get_translation('yoyo', 'fr', 'en', 'TestServiceA', user.id)
    # usage should still be zero
    quotas.get_usage_record(user.id).monthly_usage_record.characters == 0
    quotas.get_usage_record(user.id).daily_usage_record.characters == 0
    # run transformation on premium service
    translation_result_str = clt_interface.get_translation('yoyo', 'fr', 'en', 'TestServiceB', user.id)
    quotas.get_usage_record(user.id).monthly_usage_record.characters == 4
    quotas.get_usage_record(user.id).daily_usage_record.characters == 4   

    # log some usage, exceeding the daily quota
    quotas.get_usage_record(user.id).update_usage(quotas.FREE_ACCOUNT_DAILY_MAX_CHARACTERS - 3)

    # the free option should go through
    translation_result_str = clt_interface.get_translation('yoyo2', 'fr', 'en', 'TestServiceA', user.id)

    # the premium option should be blocked, should raise QuotaOverUsage
    with pytest.raises(quotas.QuotaOverUsage) as quota_exception:
        translation_result_str = clt_interface.get_translation('yoyo3', 'fr', 'en', 'TestServiceB', user.id)


@pytest.mark.django_db
def test_add_language_field(api_client, data_fixture):
    # CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES=yes pytest baserow_vocabai_plugin/cloudlanguagetools/test_clt.py -k test_add_language_field
    assert os.environ['CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES'] == 'yes'

    user, token = data_fixture.create_user_and_token()

    # update language data first
    clt_interface.update_language_data()    

    response = api_client.get(reverse('api:baserow_vocabai_plugin:translation-options'),HTTP_AUTHORIZATION=f"JWT {token}",)
    assert response.status_code == HTTP_200_OK
    pprint.pprint(response.data)    

    # create database
    # ===============

    database = data_fixture.create_database_application(user=user)
    pprint.pprint(database)

    # create table 
    # ============

    url = reverse(
        "api:database:tables:async_create", kwargs={"database_id": database.id}
    )
    response = api_client.post(
        url, {"name": "test_table_1"}, format="json", HTTP_AUTHORIZATION=f"JWT {token}"
    )
    assert response.status_code == HTTP_200_OK
    json_response = response.json()
    table_id = json_response['id']
    pprint.pprint(json_response)

    # list fields in the table
    # ========================

    url = reverse(
        "api:database:fields:list", kwargs={"table_id": table_id}
    )    
    response = api_client.get(
        url, HTTP_AUTHORIZATION=f"JWT {token}"
    )
    assert response.status_code == HTTP_200_OK
    json_response = response.json()
    pprint.pprint(json_response)

    # create french language field
    # ============================

    response = api_client.post(
        reverse("api:database:fields:list", kwargs={"table_id": table_id}),
        {"name": "french", "type": "language_text", "language": "fr"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    print('response from creating french language field:')
    pprint.pprint(response_json)
    french_field_id = response_json['id']
    assert response.status_code == HTTP_200_OK

    # create english translation field
    # ================================

    response = api_client.post(
        reverse("api:database:fields:list", kwargs={"table_id": table_id}),
        {"name": "english_trans", "type": "translation", "source_field_id": french_field_id, 'target_language': 'en', 'service': 'TestServiceA'},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    english_trans_field_id = response_json['id']
    # pprint.pprint(response_json)
    assert response.status_code == HTTP_200_OK    


    # enter some data in the french field
    # ===================================

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": table_id}),
        {f"field_{french_field_id}": "bonjour"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_row = response.json()
    assert response.status_code == HTTP_200_OK    

    pprint.pprint(response_row)

    assert response_row[f'field_{french_field_id}'] == 'bonjour'
    english_field_data = json.loads(response_row[f'field_{english_trans_field_id}'])
    assert english_field_data == {
        "text": "bonjour", "from_language_key": "fr", "to_language_key": 'en'
    }


@pytest.mark.django_db
def test_pinyin(api_client, data_fixture):
    # CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES=yes pytest baserow_vocabai_plugin/cloudlanguagetools/test_clt.py -k test_pinyin
    assert os.environ['CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES'] == 'yes'

    user, token = data_fixture.create_user_and_token()

    # update language data first
    clt_interface.update_language_data()

    # create database and table
    # =========================

    database = data_fixture.create_database_application(user=user)

    url = reverse("api:database:tables:async_create", kwargs={"database_id": database.id})
    response = api_client.post(url, {"name": "test_table_1"}, format="json", HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_200_OK
    json_response = response.json()
    table_id = json_response['id']

    # add chinese field
    # =================
    # cloudlanguagetools.languages.Language.zh_cn

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

    response = api_client.post(
        reverse("api:database:fields:list", kwargs={"table_id": table_id}),
        {
            "name": "pinyin", 
            "type": "chinese_romanization", 
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
    english_trans_field_id = response_json['id']    