import pytest
import json
from django.shortcuts import reverse
from rest_framework.status import HTTP_200_OK

from baserow_vocabai_plugin.cloudlanguagetools import clt_interface, quotas

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

