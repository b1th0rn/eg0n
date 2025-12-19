"""Forms definitions for UI app."""

from ioc_management.models import Event, Instance
from ui.include.forms import ObjectModelForm


#############################################################################
# Instance
#############################################################################

class InstanceForm(ObjectModelForm):
    """Form for the Instance model."""

    class Meta:
        """Meta options."""

        fields = ("name",)
        model = Instance


#############################################################################
# Event
#############################################################################


class EventForm(ObjectModelForm):
    """Form for the Event model."""

    class Meta:
        """Meta options."""

        fields = ("name", "description")
        model = Event
    