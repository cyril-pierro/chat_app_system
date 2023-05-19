from unittest.mock import patch

import pytest
from django.test import Client
from django.urls import reverse

client = Client()


@pytest.mark.search
def test_search_view():
    """Test Search View"""
    with patch("search.views.es") as mock_elastic:
        mock_elastic.search.return_value = {
            "hits": {"hits": [{"_source": {"USERNAME": "fiopapa"}}]}
        }
        response = client.get(reverse("search_user", args=("fiopapa",)))
        assert response.json() == [{"USERNAME": "fiopapa"}]
        assert response.status_code == 200


@pytest.mark.search
def test_all_users_view():
    """Test All users View"""
    with patch("search.views.es") as mock_elastic:
        mock_elastic.search.return_value = {
            "hits": {"hits": [{"_source": {"USERNAME": "fiopapa"}}]}
        }
        response = client.get(reverse("get_all_users"))
        assert response.json() == [{"USERNAME": "fiopapa"}]
        assert response.status_code == 200
