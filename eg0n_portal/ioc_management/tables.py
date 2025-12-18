"""Table definitions for Instance app."""

import django_tables2 as tables
from ioc_management.models import Instance
from ui.include.tables import ObjectTable

#############################################################################
# Instance
#############################################################################


class InstanceTable(ObjectTable):
    """Table definition for the Instance model."""

    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options."""

        model = Instance
        # exclude = ("id",)
        sequence = (
            "name",
            "created_at",
            "updated_at",
        )
        order_by = "name"
