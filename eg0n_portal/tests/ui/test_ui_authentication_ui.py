"""Test UI authentication."""

import pytest


@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_authentication_ui_user(client, user_sets, role):
    """Test UI authentication."""
    username = f"{role}1"
    password = f"{username}_pass"
    logged = client.login(username=username, password=password)
    assert logged is True, f"Failed for user {username} ({role})"


@pytest.mark.django_db
def test_ui_authentication_ui_guest(client, user_sets):
    """Test UI authentication by non-existent user."""
    logged = client.login(username="guest", password="guest_pass")
    assert logged is False, "Expected failed for guest login"
