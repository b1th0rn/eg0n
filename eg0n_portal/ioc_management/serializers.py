"""Serializers for IoC Management app."""

from rest_framework import serializers
from ioc_management.models import CodeSnippet, Event, FQDN, Hash, IpAdd, Vuln


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
            "lastchange_author",
            "created_at",
            "updated_at",
        )

    def perform_create(self, serializer):
        """Set user when creating a new event."""
        serializer.save(author=self.request.user)



#############################################################################
# CodeSnippet
#############################################################################


class CodeSnippetSerializer(serializers.ModelSerializer):
    """Serializer for CodeSnippet model."""

    class Meta:
        """Meta options."""

        model = CodeSnippet
        fields = "__all__"
        read_only_fields = (
            "id",
            "author",
            "contributors_authors",
            "created_at",
            "updated_at",
        )

    def perform_create(self, serializer):
        """Set user when creating a new code snippet."""
        serializer.save(author=self.request.user)


#############################################################################
# FQDN
#############################################################################


class FQDNSerializer(serializers.ModelSerializer):
    """Serializer for FQDN model."""

    class Meta:
        """Meta options."""

        model = FQDN
        fields = "__all__"
        read_only_fields = (
            "id",
            "author",
            "contributors_authors",
            "created_at",
            "updated_at",
        )

    def perform_create(self, serializer):
        """Set user when creating a new FQDN."""
        serializer.save(author=self.request.user)


#############################################################################
# Hash
#############################################################################


class HashSerializer(serializers.ModelSerializer):
    """Serializer for Hash model."""

    class Meta:
        """Meta options."""

        model = Hash
        fields = "__all__"
        read_only_fields = (
            "id",
            "author",
            "contributors_authors",
            "created_at",
            "updated_at",
        )

    def perform_create(self, serializer):
        """Set user when creating a new hash."""
        serializer.save(author=self.request.user)


#############################################################################
# IpAdd
#############################################################################


class IpAddSerializer(serializers.ModelSerializer):
    """Serializer for IpAdd model."""

    class Meta:
        """Meta options."""

        model = IpAdd
        fields = "__all__"
        read_only_fields = (
            "id",
            "author",
            "contributors_authors",
            "created_at",
            "updated_at",
        )

    def perform_create(self, serializer):
        """Set user when creating a new IP address."""
        serializer.save(author=self.request.user)


#############################################################################
# Vuln
#############################################################################


class VulnSerializer(serializers.ModelSerializer):
    """Serializer for Vuln model."""

    class Meta:
        """Meta options."""

        model = Vuln
        fields = "__all__"
        read_only_fields = (
            "id",
            "author",
            "contributors_authors",
            "created_at",
            "updated_at",
        )

    def perform_create(self, serializer):
        """Set user when creating a new vulnerability."""
        serializer.save(author=self.request.user)
