import pytest
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

    # update usage record
    usage_record = quotas.get_usage_record(user.id)
    assert usage_record.monthly_usage_record.characters == 0
    assert usage_record.daily_usage_record.characters == 0
    # quotas.log_usage
