"""Table definitions for Instance app."""

import django_tables2 as tables
from ioc_management.models import Instance
from ui.include.tables import (
    GreenRedBooleanColumn,
    GreenRedReverseBooleanColumn,
    ObjectTable,
)

#############################################################################
# Instance
#############################################################################


class InstanceTable(ObjectTable):
    """Table definition for the Instance model."""

    class Meta:
        """Meta options."""

        model = Instance
        # exclude = ("id", "password", "date_joined", "last_login")
        # sequence = (
        #     "username",
        #     "first_name",
        #     "last_name",
        #     "email",
        #     "is_active",
        #     "is_superuser",
        #     "is_staff",
        # )
        # order_by = "username"