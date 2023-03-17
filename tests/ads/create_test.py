import pytest


def test_root(client):
    response = client.get("/ad/")

    assert response.status_code == 404

@pytest.mark.django_db
def test_create_ad(client, access_token):
    data = {
            "author_id": 1,
            "category_id": 2,
            "name": "Купите Слона",
            "price": 1300,
            }

    expected = {
        "id": 1,
        "name": "Купите Слона",
        "author_id": None,
        "price": 1300.0,
        "description": None,
        "is_published": False,
        "image": None,
        "category_id": None
    }
    response = client.post("/ad/create/", data, HTTP_AUTHORIZATION="Bearer " + access_token)
    assert response.status_code == 201
    assert response.data == expected
