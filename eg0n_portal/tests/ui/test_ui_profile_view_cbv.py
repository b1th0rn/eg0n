"""Test API profile view."""

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_profile_view_cbv_user(client, user_sets, role):
    """
    Test Django model view (CBV) for user profile.
    
    Each user should be able to access their own profile page (HTML view).
    """
    user = user_sets[0][role]

    # Log in the user in the Django test client
    client.force_login(user)

    # Adjust the URL name to match your CBV route name (e.g., "user-detail-view")
    url = reverse("user_detail", kwargs={"pk": user.id})

    response = client.get(url)
    assert response.status_code == 200, f"Failed for user {user.username} ({role})"

    # Optional: check that some user data is in the rendered HTML
    assert user.username in response.content.decode(), (
        f"Username not visible in response for {role}"
    )
