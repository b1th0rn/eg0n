"""
Pytest fixtures for testing API and models.
"""

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import Group, User

@pytest.fixture
def api_client():
    """Provide a DRF APIClient instance for test requests."""
    return APIClient()


# ==============================================================================
# Users and Groups
# ==============================================================================

@pytest.fixture
def user_sets(db):
    """Create a set of users bound to the same group."""
    user_groups = []
    for i in range(1, 4):
        group_obj = Group.objects.create(name=f"group{i}")
        admin_user_obj = User.objects.create_superuser(
            username=f"admin{i}",
            email=f"admin{i}@example.com",
            password=f"admin{i}_pass",
        )
        admin_user_obj.groups.add(group_obj)

        staff_user_obj = User.objects.create_user(
            username=f"staff{i}",
            email=f"staff{i}@example.com",
            password=f"staff{i}_pass",
            is_staff=True,
        )
        staff_user_obj.groups.add(group_obj)

        user_obj = User.objects.create_user(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password=f"user{i}_pass",
            is_staff=False,
            is_superuser=False
        )
        user_obj.groups.add(group_obj)

        user_groups.append({
            "admin": admin_user_obj,
            "staff": staff_user_obj,
            "user": user_obj,
            "group": group_obj,
        })
    return user_groups
