"""Test API profile view."""

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_profile_view_api(api_client, user_sets, role):
    """Test API profile view."""
    user = user_sets[0][role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-detail", kwargs={"pk": user.id})
    response = api_client.get(url, headers=headers)
    assert response.status_code == 200
