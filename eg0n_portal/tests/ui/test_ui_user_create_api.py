"""Test API user list view."""

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_user_create_api_admin(api_client, user_sets, role):
    """Test API create user by admin."""
    user = user_sets[0][role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}

    url = reverse("user-list")
    payload = {"username": "new_user"}
    response = api_client.post(url, payload, format="json", headers=headers)
    if role == "admin":
        # Admin users must be able to create new users.
        assert response.status_code == 201, f"Failed for user {user.username}"
        assert response.data["username"] == payload["username"], f"username not set"
    else:
        # Non admin users cannot create new users.
        assert response.status_code == 403, f"Expected 401 for {user.username}"


def test_ui_user_create_api_guest(api_client, user_sets):
    """Test API get user list by guest user."""
    url = reverse("user-list")
    payload = {"username": "new_user"}
    response = api_client.post(url, payload, format="json")
    assert response.status_code == 401, "Expected 401 for guest user"
