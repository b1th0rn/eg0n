"""Test UI authentication."""

import pytest


@pytest.mark.django_db
def test_ui_authentication_ui_admin(client, user_set):
    """Test UI authentication by admin."""
    logged = client.login(username="admin1", password="admin1_pass")
    assert logged is True


@pytest.mark.django_db
def test_ui_authentication_ui_staff(client, user_set):
    """Test UI authentication by staff."""
    logged = client.login(username="staff1", password="staff1_pass")
    assert logged is True


@pytest.mark.django_db
def test_ui_authentication_ui_user(client, user_set):
    """Test UI authentication by user."""
    logged = client.login(username="user1", password="user1_pass")
    assert logged is True


@pytest.mark.django_db
def test_ui_authentication_ui_guest(client):
    """Test UI authentication by non-existent user."""
    logged = client.login(username="guest", password="guest_pass")
    assert logged is False
