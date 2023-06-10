import pytest
from rest_framework import status

from tests.factories import AdFactory


@pytest.mark.django_db
def test_selection_create(client, user_with_access_token):

    ad_list = AdFactory.create_batch(4)
    user, token = user_with_access_token
    data = {
        'name': 'Подборка',
        'owner': user.username,
        'items': [
            ad.pk for ad in ad_list
        ]
    }

    expected_data = {
        'id': 1,
        'owner': user.username,
        'name': 'Подборка',
        'items': [
            ad.pk for ad in ad_list
        ]
    }

    response = client.post("/selection/", data=data, HTTP_AUTHORIZATION=f'Bearer {token}')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_data