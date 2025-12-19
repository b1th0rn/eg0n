"""Serializers, called by API View."""

from rest_framework import serializers
from ioc_management.models import Event


#############################################################################
# Event
#############################################################################


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = (
            "id",
            "author",
            "instance",
            "lastchange_author",
            "created_at",
            "updated_at",
        )
