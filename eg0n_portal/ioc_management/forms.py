"""Forms definitions for IoC Management app."""

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

    def save(self, commit=True):
        """On form save."""
        instance = super().save(commit=False)

        instance.author = self.user
        if commit:
            instance.save()
        return instance
