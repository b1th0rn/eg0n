"""Test DRF (API) profile deletion."""

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_ui_profile_delete_api_admin(api_client, user_set_group1):
    """Test DRF (API) admin profile deletion."""
    role = "admin"
    user = user_set_group1[role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-detail", kwargs={"pk": user.id})
    response = api_client.delete(url, headers=headers)
    assert (
        response.status_code == 403
    ), f"Expected 403 for user {user.username} ({role})"
    # Verify the profile still exists
    response = api_client.get(url, headers=headers)
    assert (
        response.status_code == 200
    ), f"Expected 200 for user {user.username} ({role})"


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["staff", "user"])
def test_ui_profile_delete_api_user(api_client, user_set_group1, role):
    """Test DRF (API) non-admin profile deletion."""
    admin_token, _ = Token.objects.get_or_create(user=user_set_group1["admin"])
    admin_headers = {"Authorization": f"Token {admin_token}"}
    user = user_set_group1[role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-detail", kwargs={"pk": user.id})
    response = api_client.delete(url, headers=headers)
    assert response.status_code == 204, f"Failed for user {user.username} ({role})"
    # Verify the profile hs been deleted
    response = api_client.get(url, headers=admin_headers)
    assert (
        response.status_code == 404
    ), f"Expected 404 for for user {user.username} ({role})"
