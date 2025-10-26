"""Test API user detail view."""

from django.urls import reverse
from rest_framework.authtoken.models import Token


def test_ui_user_detail_view_api_admin(api_client, user_sets):
    """
    Test API get user detail by admin.
    
    Admin users must see all users, even from different groups.
    """
    token, _ = Token.objects.get_or_create(user=user_sets[0]["admin"])
    headers = {"Authorization": f"Token {token}"}
    for user_set in user_sets:
        for key, value in user_set.items():
            if key in ["admin", "staff", "user"]:
                url = reverse("user-detail", kwargs={"pk": value.id})
                response = api_client.get(url, headers=headers)
                assert response.status_code == 200


def test_ui_user_detail_view_api_staff(api_client, user_sets):
    """
    Test API get user detail by staff.
    
    Staff users must see all users, within the group.
    """
    token, _ = Token.objects.get_or_create(user=user_sets[0]["staff"])
    headers = {"Authorization": f"Token {token}"}
    for key, value in user_sets[0].items():
        # Staff users must see all users, within the group.
        if key in ["admin", "staff", "user"]:
            url = reverse("user-detail", kwargs={"pk": value.id})
            response = api_client.get(url, headers=headers)
            assert response.status_code == 200
    for key, value in user_sets[1].items():
        # Staff users must not see users from different groups.
        if key in ["admin", "staff", "user"]:
            url = reverse("user-detail", kwargs={"pk": value.id})
            response = api_client.get(url, headers=headers)
            assert response.status_code == 404


def test_ui_user_detail_view_api_user(api_client, user_sets):
    """
    Test API get user detail by standard user.
    
    Standard users must see all users, within the group.
    """
    token, _ = Token.objects.get_or_create(user=user_sets[0]["user"])
    headers = {"Authorization": f"Token {token}"}
    for key, value in user_sets[0].items():
        # Standard users must see all users, within the group.
        if key in ["admin", "staff", "user"]:
            url = reverse("user-detail", kwargs={"pk": value.id})
            response = api_client.get(url, headers=headers)
            assert response.status_code == 200
    for key, value in user_sets[1].items():
        # Standard users must not see users from different groups.
        if key in ["admin", "staff", "user"]:
            url = reverse("user-detail", kwargs={"pk": value.id})
            response = api_client.get(url, headers=headers)
            assert response.status_code == 404


def test_ui_user_detail_view_api_guest(api_client, user_sets):
    """Test API get user detail by guest user."""
    for key, value in user_sets[0].items():
        if key in ["admin", "staff", "user"]:
            url = reverse("user-detail", kwargs={"pk": value.id})
            response = api_client.get(url)
            assert response.status_code == 401
