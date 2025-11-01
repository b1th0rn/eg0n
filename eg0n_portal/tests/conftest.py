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

@pytest.fixture
def create_user(db):
    def make_user(username, role="user", groups=None):
        if groups is None:
            groups = []

        email=f"{username}@example.com"
        password=f"{username}123"
        is_staff=False

        if role=="admin":
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
        else:
            if role=="staff":
                is_staff=True

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=is_staff,
            )

        for group in groups:
            group = Group.objects.create(name=group)
            user.groups.add(group)

    return make_user



# ==============================================================================
# Users and Groups
# ==============================================================================

@pytest.fixture
def user_set1(db):
    return {
        # Group 1
        "group1": {
            "admin11": create_user("admin11", role="admin", group="group1"),
            "admin12": create_user("admin12", role="admin", group="group1"),
            "staff11": create_user("staff11", role="staff", group="group1"),
            "staff12": create_user("staff12", role="staff", group="group1"),
            "user11": create_user("user11", group="group1"),
            "user12": create_user("user12", group="group1"),
        },
        "group2": {
            # Group 2
            "admin21": create_user("admin21", role="admin", group="group2"),
            "staff21": create_user("staff21", role="staff", group="group2"),
            "user21": create_user("user21", group="group2"),
        },
        "ungrouped": {
            # Ungrouped
            "admin31": create_user("admin31", role="admin"),
            "staff31": create_user("staff31", role="staff"),
            "user31": create_user("user31"),
        },
    }


@pytest.fixture
def user_set_group1(db):
    return {
        "admin11": create_user("admin11", role="admin", group="group1"),
        "admin12": create_user("admin12", role="admin", group="group1"),
        "staff11": create_user("staff11", role="staff", group="group1"),
        "staff12": create_user("staff12", role="staff", group="group1"),
        "user11": create_user("user11", group="group1"),
        "user12": create_user("user12", group="group1"),
    }


@pytest.fixture
def user_set_group2(db):
    return {
        "admin21": create_user("admin21", role="admin", group="group2"),
        "staff21": create_user("staff21", role="staff", group="group2"),
        "user21": create_user("user21", group="group2"),
    }


@pytest.fixture
def user_set_ungrouped(db):
    return {
        "admin31": create_user("admin31", role="admin"),
        "staff31": create_user("staff31", role="staff"),
        "user31": create_user("user31"),
    }



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
        )
        user_obj.groups.add(group_obj)

        user_groups.append({
            "admin": admin_user_obj,
            "staff": staff_user_obj,
            "user": user_obj,
            "group": group_obj,
        })
    return user_groups
