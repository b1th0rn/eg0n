"""Table definitions for Instance app."""

import django_tables2 as tables
from ioc_management.models import Event
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
