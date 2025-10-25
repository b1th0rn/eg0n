# """Test API authentication."""

from django.urls import reverse
from rest_framework.authtoken.models import Token


def test_ui_profile_get_api(api_client, user_sets):
    """Test API get profile."""
    for user_set in user_sets:
        for key, value in user_set.items():
            if key in ["admin", "staff", "user"]:
                token, _ = Token.objects.get_or_create(user=value)
                headers = {"Authorization": f"Token {token}"}
                url = reverse("user-detail", kwargs={"pk": value.id})
                response = api_client.get(url, headers=headers)
                assert response.status_code == 200
