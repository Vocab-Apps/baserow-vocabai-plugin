import pytest
from django.shortcuts import reverse
from rest_framework.status import HTTP_200_OK


@pytest.mark.django_db
def test_1(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()

    response = api_client.get(
        reverse("api:baserow_vocabai_plugin:language-list"),
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK