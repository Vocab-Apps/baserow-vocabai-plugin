import pytest


@pytest.mark.django_db
def test_1(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()

    assert False