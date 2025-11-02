"""Test DRF (API) profile view."""

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_profile_view_api_user(api_client, user_set_group1, role):
    """Test DRF (API) user profile view."""
    user = user_set_group1[role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-detail", kwargs={"pk": user.id})
    response = api_client.get(url, headers=headers)
    assert response.status_code == 200, f"Failed for user {user.username} ({role})"
