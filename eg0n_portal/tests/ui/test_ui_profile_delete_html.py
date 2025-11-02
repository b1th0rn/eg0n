"""Test HTML (UI) profile deletion."""

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_ui_profile_delete_ui_admin(client, user_set_group1):
    """Test HTML (UI) admin profile deletion."""
    role = "admin"
    user = user_set_group1[role]
    client.force_login(user)
    url = reverse("user_delete", kwargs={"pk": user.id})
    response = client.get(url)
    assert response.status_code == 200, f"Expected 200 for user {user.username} ({role})"
    assert "Are you sure" in response.text, f"Expected confirmation page for user {user.username} ({role})"
    response = client.post(url)
    assert response.status_code == 403, f"Expected 403 for user {user.username} ({role})"
    # Verify the profile still exists
    response = client.get(url)
    assert response.status_code == 200, f"Expected 200 for user {user.username} ({role})"


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["staff", "user"])
def test_ui_profile_delete_cbv_user(client, admin_client, user_set_group1, role):
    """Test HTML (UI) non-admin profile deletion."""
    admin = user_set_group1["admin"]
    admin_client.force_login(admin)
    user = user_set_group1[role]
    client.force_login(user)
    url = reverse("user_delete", kwargs={"pk": user.id})
    response = client.get(url)
    assert response.status_code == 200, f"Expected 200 for user {user.username} ({role})"
    assert "Are you sure" in response.text, f"Expected confirmation page for user {user.username} ({role})"
    response = client.post(url)
    assert response.status_code == 302, f"Expected 302 for user {user.username} ({role})"
    # Verify the profile hs been deleted
    response = admin_client.get(url)
    assert response.status_code == 404, f"Expected 404 for for user {user.username} ({role})"
