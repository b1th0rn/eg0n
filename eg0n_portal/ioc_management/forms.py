"""Forms definitions for IoC Management app."""

from ioc_management.models import Event, CodeSnippet, FQDN, Hash, IpAdd, Vuln
from ui.include.forms import ObjectModelForm


#############################################################################
# Generic Attribute Mixin
#############################################################################


class AttributeFormMixin:
    """Standard actions for generic attributes."""

    def save(self, commit=True):
        """On form save."""
        instance = super().save(commit=False)

        if not self.instance.pk:
            # New Attribute
            instance.author = self.user

        if not (instance.author != self.user and instance.contributors.filter(id=self.user.pk)):
            # Add user as contributor
            instance.contributors.add(self.user)

        if commit:
            instance.save()
            instance.event.save()
        return instance
    

#############################################################################
# Event
#############################################################################


class EventForm(ObjectModelForm):
    """Form for the Event model."""

    class Meta:
        """Meta options."""

        fields = ("name", "description")
        model = Event

    def save(self, commit=True):
        """On form save."""
        instance = super().save(commit=False)

        if not self.instance.pk:
            # New Event
            instance.author = self.user

        if not (instance.author != self.user and instance.contributors.filter(id=self.user.pk)):
            # Add user as contributor
            instance.contributors.add(self.user)

        if commit:
            instance.save()
        return instance


#############################################################################
# CodeSnippet
#############################################################################


class CodeSnippetForm(AttributeFormMixin, ObjectModelForm):
    """Form for the CodeSnippet model."""

    class Meta:
        """Meta options."""

        fields = ("name", "language", "code", "confidence", "validation_status", "description", "expired_at")
        model = CodeSnippet


#############################################################################
# FQDN
#############################################################################


class FQDNForm(AttributeFormMixin, ObjectModelForm):
    """Form for the Vuln model."""

    class Meta:
        """Meta options."""

        fields = ("fqdn", "confidence", "validation_status", "description", "expired_at")
        model = FQDN


#############################################################################
# Hash
#############################################################################


class HashForm(AttributeFormMixin, ObjectModelForm):
    """Form for the Vuln model."""

    class Meta:
        """Meta options."""

        fields = ("filename", "md5", "sha1", "sha256", "platform", "url", "confidence", "validation_status", "description", "expired_at")
        model = Hash


#############################################################################
# IpAdd
#############################################################################


class IpAddForm(AttributeFormMixin, ObjectModelForm):
    """Form for the Vuln model."""

    class Meta:
        """Meta options."""

        fields = ("ip_address", "confidence", "validation_status", "description", "expired_at")
        model = IpAdd


#############################################################################
# Vuln
#############################################################################


class VulnForm(AttributeFormMixin, ObjectModelForm):
    """Form for the Vuln model."""

    class Meta:
        """Meta options."""

        fields = ("cve", "name", "cvss", "description")
        model = Vuln

