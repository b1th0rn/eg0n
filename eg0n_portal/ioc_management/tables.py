"""Table definitions for IoC Management app."""

import django_tables2 as tables
from ioc_management.models import Event, CodeSnippet, FQDN, Hash, IpAdd, Vuln
from ui.include.tables import ObjectTable


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

    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = CodeSnippet
        # exclude = ("id", "description", "lastchange_author")
        # sequence = (
        #     "name",
        #     "author",   
        #     "created_at",
        #     "updated_at",
        # )
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

    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = FQDN
        # exclude = ("id", "description", "lastchange_author")
        # sequence = (
        #     "name",
        #     "author",   
        #     "created_at",
        #     "updated_at",
        # )
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

    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = Hash
        # exclude = ("id", "description", "lastchange_author")
        # sequence = (
        #     "name",
        #     "author",   
        #     "created_at",
        #     "updated_at",
        # )
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

    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = IpAdd
        # exclude = ("id", "description", "lastchange_author")
        # sequence = (
        #     "name",
        #     "author",   
        #     "created_at",
        #     "updated_at",
        # )
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

    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = Vuln
        # exclude = ("id", "description", "lastchange_author")
        # sequence = (
        #     "name",
        #     "author",   
        #     "created_at",
        #     "updated_at",
        # )
        order_by = "-updated_at"
        attrs = {
            "search": False,
            "table_actions": [],
            "row_actions": [],
        }
