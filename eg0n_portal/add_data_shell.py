#!/usr/bin/env python3

"""
Pytest fixtures for testing API and models.
"""

from django.contrib.auth.models import Group, User


for i in range(1, 4):
    group_obj, _ = Group.objects.get_or_create(name=f"group{i}")

    admin_user_obj = User.objects.filter(username=f"admin{i}").first()
    if not admin_user_obj:
        admin_user_obj = User.objects.create_superuser(
            username=f"admin{i}",
            email=f"admin{i}@example.com",
            password=f"admin{i}_pass",
        )
    admin_user_obj.groups.add(group_obj)

    staff_user_obj = User.objects.filter(username=f"staff{i}").first()
    if not staff_user_obj:
        staff_user_obj = User.objects.create_user(
            username=f"staff{i}",
            email=f"staff{i}@example.com",
            password=f"staff{i}_pass",
            is_staff=True,
        )
    staff_user_obj.groups.add(group_obj)

    user_obj = User.objects.filter(username=f"user{i}").first()
    if not user_obj:
        user_obj = User.objects.create_user(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password=f"user{i}_pass",
        )
    user_obj.groups.add(group_obj)
