"""Test API user update."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_ui_user_update_api_admin(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user update by admin."""
    user = user_set_group_multiple["admin1"]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile deletion tested in profile tests
            continue
        url = reverse("user-detail", kwargs={"pk": u.id})
        payload = {"first_name": f"First {u.username} Name"}
        response = api_client.patch(url, payload, format="json", headers=headers)
        assert (
            response.status_code == 200
        ), f"Failed updating {u.username} by {user.username}"
        assert (
            response.data["first_name"] == payload["first_name"]
        ), f"Unexpected value for {u.username}"


@pytest.mark.django_db
def test_ui_user_read_detail_api_staff(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user detail view by staffs."""
    user = user_set_group_multiple["staff1"]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile deletion tested in profile tests
            continue
        shared_groups = bool(
            user.groups.values_list("id", flat=True)
            & u.groups.values_list("id", flat=True)
        )
        url = reverse("user-detail", kwargs={"pk": u.id})
        payload = {"first_name": f"First {u.username} Name"}
        response = api_client.patch(url, payload, format="json", headers=headers)
        if shared_groups and (u.is_superuser or u.is_staff):
            assert (
                response.status_code == 403
            ), f"User {u.username} must not be updated by {user.username}"
        elif shared_groups:
            assert (
                response.status_code == 200
            ), f"Failed updating {u.username} by {user.username}"
            assert (
                response.data["first_name"] == payload["first_name"]
            ), f"Unexpected value for {u.username}"
        else:
            assert (
                response.status_code == 404
            ), f"User {u.username} must not be updated by {user.username}"


@pytest.mark.django_db
def test_ui_user_update_detail_api_user(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user update view by users."""
    user = user_set_group_multiple["user1"]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile deletion tested in profile tests
            continue
        shared_groups = bool(
            user.groups.values_list("id", flat=True)
            & u.groups.values_list("id", flat=True)
        )
        url = reverse("user-detail", kwargs={"pk": u.id})
        response = api_client.delete(url, headers=headers)
        if shared_groups:
            assert (
                response.status_code == 403
            ), f"User {u.username} must not be update by {user.username}"
        else:
            assert (
                response.status_code == 404
            ), f"User {u.username} must not be updated by {user.username}"
