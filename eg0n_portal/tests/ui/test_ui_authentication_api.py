"""Test API authentication."""

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_authentication_api_user(api_client, user_sets, role):
    """Test API authentication."""
    user = user_sets[0][role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-list")
    response = api_client.get(url, headers=headers)
    assert response.status_code == 200, f"Failed for user {user.username} ({role})"


def test_ui_authentication_api_guest(api_client, user_sets):
    """Test UI authentication by non-existent user."""
    url = reverse("user-list")
    data = {"username": "guest", "password": "guest_pass"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 401, "Expected 401 for guest user"
