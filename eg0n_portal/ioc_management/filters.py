"""Filter definitions for IoC Management app."""

from django import forms
import django_filters
from ioc_management.models import Event
from ui.include.filters import SearchFilterSet


#############################################################################
# Event
#############################################################################


class EventFilter(SearchFilterSet):
    """Filter class for the Event model."""

    search_fields = ("name", "description")
    created_at__gte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Created after",
    )
    created_at__lte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Created before",
    )
    updated_at__gte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Updated after",
    )
    updated_at__lte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Updated before",
    )

    class Meta:
        model = Event
        fields = (
            "author",
            "contributors_authors",
            "created_at__gte",
            "created_at__lte",
            "updated_at__gte",
            "updated_at__lte",
        )
    