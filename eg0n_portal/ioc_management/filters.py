"""Filter definitions for Instance app."""

from ioc_management.models import Instance
from ui.include.filters import SearchFilterSet


class InstanceFilter(SearchFilterSet):
    """Filter class for the Instance model."""

    search_fields = ("name",)
