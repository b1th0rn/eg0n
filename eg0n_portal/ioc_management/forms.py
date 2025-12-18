"""Forms definitions for UI app."""

from django import forms
from ioc_management.models import Instance
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