"""Test API profile deletion."""

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


def test_ui_profile_delete_api_admin(api_client, user_sets):
    """Test API delete admin profile."""
    user = user_sets[0]["admin"]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-detail", kwargs={"pk": user.id})
    response = api_client.delete(url, headers=headers)
    assert response.status_code == 403, "Expected 403 for admin deletion"


@pytest.mark.parametrize("role", ["staff", "user"])
def test_ui_profile_delete_api_user(api_client, user_sets, role):
    """Test API delete user profile."""
    admin_token, _ = Token.objects.get_or_create(user=user_sets[0]["admin"])
    admin_headers = {"Authorization": f"Token {admin_token}"}
    user = user_sets[0][role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-detail", kwargs={"pk": user.id})
    response = api_client.delete(url, headers=headers)
    assert response.status_code == 204, f"Failed for user {user.username} ({role})"
    # Verify the user doesn't exist anymore
    get_response = api_client.get(url, headers=admin_headers)
    assert get_response.status_code == 404, f"User {user.username} ({role}) still exists"
