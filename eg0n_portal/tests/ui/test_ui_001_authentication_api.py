"""Test DRF (API) authentication."""

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_authentication_api_user(api_client, user_set_group1, role):
    """Test DRF (API) user authentication."""
    user = user_set_group1[role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-list")
    response = api_client.get(url, headers=headers)
    assert response.status_code == 200, f"Failed for user {user.username} ({role})"


@pytest.mark.django_db
def test_ui_authentication_api_guest(api_client):
    """Test DRF (API) guest authentication."""
    url = reverse("user-list")
    response = api_client.get(url)
    assert response.status_code == 401, "Expected 401 for guest user"
