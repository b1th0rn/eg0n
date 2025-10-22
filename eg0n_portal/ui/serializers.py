"""Serializers for Group and User models.

These serializers are used by the API views to convert model
instances to and from JSON representations.
"""

from django.contrib.auth.models import Group, User
from rest_framework import serializers
from ui.include.serializers import ObjectSerializer


#############################################################################
# Group
#############################################################################


class GroupSerializer(ObjectSerializer):
    """Serializer for the `Group` model."""

    class Meta:
        model = Group
        fields = ("id", "name")


#############################################################################
# User
#############################################################################

class UserSerializer(ObjectSerializer):
    """Serializer for the `User` model."""
    groups_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "date_joined",
            "email",
            "first_name",
            "groups_display",
            "groups",
            "id",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "last_name",
            "username",
        )
        read_only_fields = (
            "date_joined",
            "groups_display",
            "id",
            "last_login",
            "password",
        )


    def get_groups_display(self, obj):
        """Ritorna i nomi dei gruppi dell'utente in formato leggibile."""
        return [{"id": group.id, "name": group.name} for group in obj.groups.all().order_by("name")]

    def update(self, instance, validated_data):
        """
        Update the user instance.

        Args:
            instance (User): The existing user instance to update.
            validated_data (dict): Validated fields from the request.

        Returns:
            User: The updated user instance.

        Behavior:
            - Updates all standard fields from `validated_data`.
            - If a `password` key is provided, it is set via
              `set_password()` to ensure hashing.
            - Saves the instance before returning.
        """
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:  # if filled in
            instance.set_password(password)

        instance.save()
        return instance
