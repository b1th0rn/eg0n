"""Table definitions for IoC Management app."""

from django.utils.translation import gettext_lazy as _
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
        exclude = ("id", "description", "lastchange_author")
        sequence = (
            "name",
            "author",   
            "created_at",
            "updated_at",
        )
        order_by = "-updated_at"


#############################################################################
# CodeSnippet
#############################################################################


class CodeSnippetTable(ObjectTable):
    """Table definition for the CodeSnippet model."""

    name = tables.LinkColumn("codesnippet_detail", args=[tables.A("pk")])
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = CodeSnippet
        exclude = ("id", "created_at", "description", "code", "confidence", "validation_status", "event", "expire_date")
        sequence = (
            "name",
            "language",
            "author",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "search": False,
            "table_actions": [],
            "row_actions": [],
        }


class CodeSnippetEmbeddedTable(ObjectTable):
    """Embedded table definition for the CodeSnippet model."""

    name = tables.LinkColumn("codesnippet_detail", args=[tables.A("pk")])
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = CodeSnippet
        exclude = ("select", "id", "author", "description", "code", "confidence", "validation_status", "event", "expire_date")
        sequence = (
            "name",
            "language",
            "created_at",
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

    fqdn = tables.LinkColumn("fqdn_detail", args=[tables.A("pk")])
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = FQDN
        exclude = ("id", "created_at", "confidence", "expire_date", "event", "validation_status", "description", "lastchange_author")
        sequence = (
            "fqdn",
            "author",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "search": False,
            "table_actions": [],
            "row_actions": [],
        }


class FQDNEmbeddedTable(ObjectTable):
    """Embedded table definition for the FQDN model."""

    fqdn = tables.LinkColumn("fqdn_detail", args=[tables.A("pk")])
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = FQDN
        exclude = ("select", "id", "author", "confidence", "expire_date", "event", "validation_status", "description", "lastchange_author")
        sequence = (
            "fqdn",
            "created_at",
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

    filename = tables.LinkColumn("hash_detail", args=[tables.A("pk")])
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = Hash
        exclude = ("id", "created_at", "confidence", "event", "description", "lastchange_author", "validation_status", "md5", "sha1", "sha256", "expire_date")
        sequence = (
            "filename",
            "platform",
            "url",
            "author",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "search": False,
            "table_actions": [],
            "row_actions": [],
        }


class HashEmbeddedTable(ObjectTable):
    """Embedded table definition for the Hash model."""

    filename = tables.LinkColumn("hash_detail", args=[tables.A("pk")])
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = Hash
        exclude = ("select", "id", "author", "confidence", "event", "description", "lastchange_author", "validation_status", "md5", "sha1", "sha256", "expire_date")
        sequence = (
            "filename",
            "platform",
            "url",
            "created_at",
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
        exclude = ("id", "description", "lastchange_author", "created_at", "confidence", "expire_date", "validation_status")
        sequence = (
            "ip_address",
            "event",
            "author",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "search": False,
            "table_actions": [],
            "row_actions": [],
        }


class IpAddEmbeddedTable(ObjectTable):
    """Embedded table definition for the IpAdd model."""

    ip_address = tables.LinkColumn("ipadd_detail", args=[tables.A("pk")])
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = IpAdd
        exclude = ("id", "select", "created_at", "description", "lastchange_author", "author", "confidence", "event", "expire_date", "validation_status")
        sequence = (
            "ip_address",
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
        exclude = ("id", "name", "description", "lastchange_author", "created_at", "exploitation_details", "created_at")
        sequence = (
            "cve",
            "event",
            "cvss",   
            "author",
            "updated_at",
        )
        order_by = "-updated_at"
        attrs = {
            "search": False,
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
        exclude = ("id", "select", "description", "lastchange_author", "author", "event", "exploitation_details", "created_at")
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
