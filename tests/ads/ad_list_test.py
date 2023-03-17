import pytest

from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_list(client, access_token):
    ad_list = AdFactory.create_batch(3)

    response = client.get("/ad/", HTTP_AUTHORIZATION="Bearer " + access_token)
    assert response.status_code == 200

