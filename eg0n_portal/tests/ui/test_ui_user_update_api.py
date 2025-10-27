"""Test API user list view."""

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def test_ui_user_update_api_admin(api_client, user_sets):
    """
    Test API update user by admin.
    
    Admin users must see all users, even from different groups.
    """
    token, _ = Token.objects.get_or_create(user=user_sets[0]["admin"])
    headers = {"Authorization": f"Token {token}"}
    for user_set in user_sets:
        for key, value in user_set.items():
            if key in ["admin", "staff", "user"]:
                if user_sets[0]["admin"].id == value.id:
                    # Same user
                    continue
                url = reverse("user-detail", kwargs={"pk": value.id})
                payload = {"first_name": f"First {key} Name", "last_name": f"Last {key} Name"}
                response = api_client.patch(url, payload, format="json", headers=headers)
                assert response.status_code == 200, f"Failed for user {value.username}"
                assert response.data["first_name"] == payload["first_name"], f"first_name not updated for user {value.username}"
                assert response.data["last_name"] == payload["last_name"], f"last_name not updated for user {value.username}"
                
        

def test_ui_user_update_api_staff(api_client, user_sets):
    """
    Test API update user list by staff.
    
    Staff users must see all users, within the group.
    """
    token, _ = Token.objects.get_or_create(user=user_sets[0]["staff"])
    headers = {"Authorization": f"Token {token}"}
    # Adding an additional staff user
    extra_staff = User.objects.create_user(
        username="extra",
        password="extra_pass",
        is_staff=True,
    )
    extra_staff.groups.add(user_sets[0]["user"].groups.first())
    for key, value in user_sets[0].items():
        # Staff users must see all users, within the group.
        if key in ["admin"]:
            url = reverse("user-detail", kwargs={"pk": value.id})
            payload = {"first_name": f"First {key} Name", "last_name": f"Last {key} Name"}
            response = api_client.patch(url, payload, format="json", headers=headers)
            assert response.status_code == 403, "Expected 403 for admin users"
        if key in ["user"]:
            url = reverse("user-detail", kwargs={"pk": value.id})
            payload = {"first_name": f"First {key} Name", "last_name": f"Last {key} Name"}
            response = api_client.patch(url, payload, format="json", headers=headers)
            assert response.status_code == 200, f"Failed for user {value.username}"
            assert response.data["first_name"] == payload["first_name"], f"first_name not updated for user {value.username}"
            assert response.data["last_name"] == payload["last_name"], f"last_name not updated for user {value.username}"
    url = reverse("user-detail", kwargs={"pk": extra_staff.id})
    payload = {"first_name": f"First extra Name", "last_name": f"Last extra Name"}
    response = api_client.patch(url, payload, format="json", headers=headers)
    assert response.status_code == 403, "Expected 403 for staff users"
    for key, value in user_sets[1].items():
        # Staff users must not see users from different groups.
        if key in ["admin", "staff", "user"]:
            url = reverse("user-detail", kwargs={"pk": value.id})
            payload = {"first_name": f"First {key} Name", "last_name": f"Last {key} Name"}
            response = api_client.patch(url, payload, format="json", headers=headers)
            assert response.status_code == 404, "Expected 404 for user on diffenret group"


def test_ui_user_update_api_user(api_client, user_sets):
    """
    Test API get user list by standard user.
    
    Standard users must see all users, within the group.
    """
    token, _ = Token.objects.get_or_create(user=user_sets[0]["user"])
    headers = {"Authorization": f"Token {token}"}
    # Adding an additional stanard user
    extra_user = User.objects.create_user(
        username="extra",
        password="extra_pass",
    )
    extra_user.groups.add(user_sets[0]["user"].groups.first())
    for key, value in user_sets[0].items():
        # Standard users must see all users, within the group.
        if key in ["admin", "staff"]:
            url = reverse("user-detail", kwargs={"pk": value.id})
            payload = {"first_name": f"First {key} Name", "last_name": f"Last {key} Name"}
            response = api_client.patch(url, payload, format="json", headers=headers)
            assert response.status_code == 403, f"Failed for user {value.username}"
    url = reverse("user-detail", kwargs={"pk": extra_user.id})
    payload = {"first_name": f"First extra Name", "last_name": f"Last extra Name"}
    response = api_client.patch(url, payload, format="json", headers=headers)
    assert response.status_code == 403, f"Failed for user {value.username}"
    for key, value in user_sets[1].items():
        # Standard users must not see users from different groups.
        if key in ["admin", "staff", "user"]:
            url = reverse("user-detail", kwargs={"pk": value.id})
            payload = {"first_name": f"First {key} Name", "last_name": f"Last {key} Name"}
            response = api_client.patch(url, payload, format="json", headers=headers)
            assert response.status_code == 404, "Expected 404 for user on diffenret group"


def test_ui_user_update_api_guest(api_client, user_sets):
    """Test API get user list by guest user."""
    for key, value in user_sets[0].items():
        if key in ["admin", "staff", "user"]:
            url = reverse("user-detail", kwargs={"pk": value.id})
            payload = {"first_name": f"First Name", "last_name": f"Last Name"}
            response = api_client.patch(url, payload, format="json")
            assert response.status_code == 401, "Expected 401 for guest user"
