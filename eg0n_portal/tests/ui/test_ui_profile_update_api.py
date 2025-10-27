"""Test API profile update."""

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_profile_update_api_user(api_client, user_sets, role):
    """Test API update profile."""
    user = user_sets[0][role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-detail", kwargs={"pk": user.id})
    payload = {"first_name": f"New {user.username} Name"}
    response = api_client.patch(url, payload, format="json", headers=headers)
    assert response.status_code == 200, f"Failed for user {user.username} ({role})"
    assert response.data["first_name"] == payload["first_name"], f"Mismatch for user {user.username} ({role})"
