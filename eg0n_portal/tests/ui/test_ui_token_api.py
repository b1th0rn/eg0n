"""Test API authentication."""

from django.urls import reverse


def test_ui_authentication_token_api_admin(api_client, user_sets):
    """Test API token creation by admin."""
    url = reverse("api_token")
    data = {"username": "admin1", "password": "admin1_pass"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 200
    assert "token" in response.data
    assert len(response.data["token"]) > 0


def test_ui_authentication_token_api_staff(api_client, user_sets):
    """Test API token creation by staff."""
    url = reverse("api_token")
    data = {"username": "staff1", "password": "staff1_pass"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 200
    assert "token" in response.data
    assert len(response.data["token"]) > 0


def test_ui_authentication_token_api_user(api_client, user_sets):
    """Test API token creation by user."""
    url = reverse("api_token")
    data = {"username": "user1", "password": "user1_pass"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 200
    assert "token" in response.data
    assert len(response.data["token"]) > 0


def test_ui_authentication_token_api_guest(api_client, user_sets):
    """Test UI token creation by non-existent user."""
    url = reverse("api_token")
    data = {"username": "guest", "password": "guest_pass"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
