"""Test API token creation."""

import pytest
from django.urls import reverse


@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_authentication_token_create_api_user(api_client, user_sets, role):
    """Test API token creation."""
    username = f"{role}1"
    password = f"{username}_pass"
    url = reverse("api_token")
    data = {"username": username, "password": password}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 200, f"Failed for user {username} ({role})"
    assert len(response.data["token"]) > 0, f"Missing token for user {username} ({role})"


def test_ui_authentication_token_create_api_guest(api_client, user_sets):
    """Test UI token creation by non-existent user."""
    url = reverse("api_token")
    data = {"username": "guest", "password": "guest_pass"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400, "Expected 400 for guest user"
