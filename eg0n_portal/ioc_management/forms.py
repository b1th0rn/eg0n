"""Forms definitions for UI app."""

from ioc_management.models import Event
from ui.include.forms import ObjectModelForm


#############################################################################
# Event
#############################################################################


class EventForm(ObjectModelForm):
    """Form for the Event model."""

    class Meta:
        """Meta options."""

        fields = ("name", "description")
        model = Event
    