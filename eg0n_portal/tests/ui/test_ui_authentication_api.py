"""Test API authentication."""

from django.urls import reverse
from rest_framework.authtoken.models import Token


def test_ui_authentication_api_admin(api_client, user_sets):
    """Test API authentication by admin."""
    token, _ = Token.objects.get_or_create(user=user_sets[0]["admin"])
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-list")
    response = api_client.get(url, headers=headers)
    assert response.status_code == 200


def test_ui_authentication_api_staff(api_client, user_sets):
    """Test API authentication by staff."""
    token, _ = Token.objects.get_or_create(user=user_sets[0]["staff"])
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-list")
    response = api_client.get(url, headers=headers)
    assert response.status_code == 200


def test_ui_authentication_api_user(api_client, user_sets):
    """Test API authentication by user."""
    token, _ = Token.objects.get_or_create(user=user_sets[0]["user"])
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-list")
    response = api_client.get(url, headers=headers)
    assert response.status_code == 200


def test_ui_authentication_api_token_guest(api_client, db):
    """Test UI authentication by non-existent user."""
    url = reverse("user-list")
    data = {"username": "guest", "password": "guest_pass"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 401
