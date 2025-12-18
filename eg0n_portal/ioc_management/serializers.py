"""Serializers, called by API View."""

from rest_framework import serializers
from ioc_management.models import Event, Instance


#############################################################################
# Instance
#############################################################################


class InstanceSerializer(serializers.ModelSerializer):
    """Serializer for Instance model."""

    class Meta:
        model = Instance
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "updated_at",
        )


#############################################################################
# Event
#############################################################################


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "updated_at",
        )
