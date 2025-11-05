"""Test API user update."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_role_upgrade_api(api_client, user_set_group1, role):
    """Test DRF (API) role upgrade."""
    user = user_set_group1[role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    for u in User.objects.all():
        payload = {"is_superuser": True, "is_staff": True}
        url = reverse("user-detail", kwargs={"pk": u.id})
        response = api_client.patch(url, payload, format="json", headers=headers)
        if role == "admin" and not u.is_superuser:
            # Admins can upgrade users
            v = User.objects.get(id=u.id)
            assert (
                v.is_superuser
            ), f"Failed upgrading {u.username} by {user.username}" + str(response.text)
        if role in ("staff", "user") and not u.is_superuser:
            # Staff cannot upgrade users
            v = User.objects.get(id=u.id)
            assert (
                not v.is_superuser
            ), f"User {u.username} cannot be upgraded by {user.username}"
        if role in ("staff", "user") and not u.is_staff:
            # Staff cannot upgrade users
            v = User.objects.get(id=u.id)
            assert (
                not v.is_staff
            ), f"User {u.username} cannot be upgraded by {user.username}"
