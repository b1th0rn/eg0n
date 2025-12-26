"""Table definitions for IoC Management app."""

from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.safestring import mark_safe
import django_tables2 as tables
from ioc_management.models import Event, CodeSnippet, FQDN, Hash, IpAdd, Vuln
from ui.include.tables import ObjectTable, GreenRedDateInTheFuture


#############################################################################
# Event
#############################################################################


class EventTable(ObjectTable):
    """Table definition for the Event model."""

    name = tables.LinkColumn("event_detail", args=[tables.A("pk")])
    author = tables.LinkColumn("user_detail", args=[tables.A("author__pk")])
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = Event
        exclude = ("id", "description", "select")
        sequence = (
            "name",
            "author",   
            "created_at",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "row_actions": [],
        }


class OwnedEventHomeTable(ObjectTable):
    """Dashboard owned Table definition for the Event model."""

    name = tables.LinkColumn("event_detail", args=[tables.A("pk")])
    contributors = tables.Column(
        accessor="contributors.all",
        orderable=False,
    )
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = Event
        exclude = ("select", "id", "description", "select", "author")
        sequence = (
            "name",
            "contributors",   
            "created_at",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "title": "Owned events",
            "search": False,
            "table_actions": [],
            "row_actions": [],
        }

    def render_contributors(self, value, record):
        """Print each contributor with link."""
        links = []
        for user in value:
            url = reverse("event_list") + f"?user={user.pk}"
            links.append(f'<a href="{url}">{user.username}</a>')
        return mark_safe(", ".join(links))
    

class ContributedEventHomeTable(ObjectTable):
    """Dashboard contributed Table definition for the Event model."""

    name = tables.LinkColumn("event_detail", args=[tables.A("pk")])
    author = tables.LinkColumn(
        "event_list",
        accessor="author",
        attrs={
            "a": {
                "href": lambda record: reverse("event_list") + f"?user={record.author.pk}"
            }
        }
    )
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = Event
        exclude = ("select", "id", "description", "select")
        sequence = (
            "name",
            "author",   
            "created_at",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "title": "Contributed events",
            "search": False,
            "table_actions": [],
            "row_actions": [],
        }

    
#############################################################################
# CodeSnippet
#############################################################################


class CodeSnippetTable(ObjectTable):
    """Table definition for the CodeSnippet model."""

    author = tables.LinkColumn("user_detail", args=[tables.A("author__pk")])
    event = tables.LinkColumn("event_detail", args=[tables.A("event__pk")])
    name = tables.LinkColumn("codesnippet_detail", args=[tables.A("pk")])
    expired_at = GreenRedDateInTheFuture(verbose_name="Valid")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = CodeSnippet
        exclude = ("id", "select", "created_at", "description", "code", "confidence", "validation_status")
        sequence = (
            "name",
            "language",
            "event",
            "author",
            "expired_at",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "table_actions": [],
            "row_actions": [],
        }


class CodeSnippetEmbeddedTable(ObjectTable):
    """Embedded table definition for the CodeSnippet model."""

    name = tables.LinkColumn("codesnippet_detail", args=[tables.A("pk")])
    expired_at = GreenRedDateInTheFuture(verbose_name="Valid")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = CodeSnippet
        exclude = ("select", "id", "author", "description", "code", "created_at", "event")
        sequence = (
            "name",
            "language",
            "confidence",
            "validation_status",
            "expired_at",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "search": False,
            "table_actions": [],
            "row_actions": [],
        }

#############################################################################
# FQDN
#############################################################################


class FQDNTable(ObjectTable):
    """Table definition for the FQDN model."""

    author = tables.LinkColumn("user_detail", args=[tables.A("author__pk")])
    event = tables.LinkColumn("event_detail", args=[tables.A("event__pk")])
    fqdn = tables.LinkColumn("fqdn_detail", args=[tables.A("pk")])
    expired_at = GreenRedDateInTheFuture(verbose_name="Valid")
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = FQDN
        exclude = ("id", "select", "created_at", "confidence", "validation_status", "description")
        sequence = (
            "fqdn",
            "event",
            "author",
            "expired_at",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "table_actions": [],
            "row_actions": [],
        }


class FQDNEmbeddedTable(ObjectTable):
    """Embedded table definition for the FQDN model."""

    fqdn = tables.LinkColumn("fqdn_detail", args=[tables.A("pk")])
    expired_at = GreenRedDateInTheFuture(verbose_name="Valid")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = FQDN
        exclude = ("select", "id", "author", "event", "created_at", "description")
        sequence = (
            "fqdn",
            "confidence",
            "validation_status",
            "expired_at",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "search": False,
            "table_actions": [],
            "row_actions": [],
        }


#############################################################################
# Hash
#############################################################################


class HashTable(ObjectTable):
    """Table definition for the Hash model."""

    author = tables.LinkColumn("user_detail", args=[tables.A("author__pk")])
    event = tables.LinkColumn("event_detail", args=[tables.A("event__pk")])
    filename = tables.LinkColumn("hash_detail", args=[tables.A("pk")])
    expired_at = GreenRedDateInTheFuture(verbose_name="Valid")
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = Hash
        exclude = ("id", "select", "created_at", "url", "confidence", "description", "validation_status", "md5", "sha1", "sha256")
        sequence = (
            "filename",
            "platform",
            "event",
            "author",
            "expired_at",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "table_actions": [],
            "row_actions": [],
        }


class HashEmbeddedTable(ObjectTable):
    """Embedded table definition for the Hash model."""

    filename = tables.LinkColumn("hash_detail", args=[tables.A("pk")])
    expired_at = GreenRedDateInTheFuture(verbose_name="Valid")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = Hash
        exclude = ("select", "id", "author", "created_at", "event", "description", "md5", "sha1", "sha256")
        sequence = (
            "filename",
            "platform",
            "url",
            "confidence",
            "validation_status",
            "expired_at",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "search": False,
            "table_actions": [],
            "row_actions": [],
        }


#############################################################################
# IpAdd
#############################################################################


class IpAddTable(ObjectTable):
    """Table definition for the IpAdd model."""

    author = tables.LinkColumn("user_detail", args=[tables.A("author__pk")])
    event = tables.LinkColumn("event_detail", args=[tables.A("event__pk")])
    ip_address = tables.LinkColumn("ipadd_detail", args=[tables.A("pk")])
    expired_at = GreenRedDateInTheFuture(verbose_name="Valid")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = IpAdd
        exclude = ("id", "select", "description", "created_at", "confidence", "validation_status")
        sequence = (
            "ip_address",
            "event",
            "author",
            "expired_at",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "table_actions": [],
            "row_actions": [],
        }


class IpAddEmbeddedTable(ObjectTable):
    """Embedded table definition for the IpAdd model."""

    ip_address = tables.LinkColumn("ipadd_detail", args=[tables.A("pk")])
    expired_at = GreenRedDateInTheFuture(verbose_name="Valid")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = IpAdd
        exclude = ("id", "select", "created_at", "description", "author", "event")
        sequence = (
            "ip_address",
            "confidence",
            "validation_status",
            "expired_at",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "search": False,
            "table_actions": [],
            "row_actions": [],
        }


#############################################################################
# Vuln
#############################################################################


class VulnTable(ObjectTable):
    """Table definition for the Vuln model."""

    author = tables.LinkColumn("user_detail", args=[tables.A("author__pk")])
    event = tables.LinkColumn("event_detail", args=[tables.A("event__pk")])
    cve = tables.LinkColumn("vuln_detail", args=[tables.A("pk")])
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = Vuln
        exclude = ("id", "select", "name", "description", "created_at", "exploitation_details", "created_at")
        sequence = (
            "cve",
            "cvss",   
            "event",
            "author",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "table_actions": [],
            "row_actions": []
        }

class VulnEmbeddedTable(ObjectTable):
    """Embedded table definition for the Vuln model."""

    name = tables.LinkColumn("vuln_detail", args=[tables.A("pk")])
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = Vuln
        exclude = ("id", "select", "description", "author", "event", "exploitation_details", "created_at")
        sequence = (
            "name",
            "cve",
            "cvss",   
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "search": False,
            "table_actions": [],
            "row_actions": [],
        }
