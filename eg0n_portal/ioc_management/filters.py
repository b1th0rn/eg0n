"""Filter definitions for IoC Management app."""

from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
import django_filters
from ioc_management.models import Event, PLATFORM_CHOICES, LANGUAGES_CHOICES, VALIDATION_CHOICES, CONFIDENCE_CHOICES, CodeSnippet, Hash, IpAdd, FQDN, Vuln
from ui.include.filters import SearchFilterSet


#############################################################################
# Event
#############################################################################


class EventFilter(SearchFilterSet):
    """Filter class for the Event model."""

    search_fields = ("name", "description")
    user = django_filters.ModelChoiceFilter(
        field_name="author",  # placeholder
        queryset=User.objects.all(),
        method="filter_user",
        label="User",
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
            "user",
            "updated_at__gte",
            "updated_at__lte",
        )

    def filter_user(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(author=value) | Q(contributors=value)
        ).distinct()


#############################################################################
# CodeSnippet
#############################################################################


class CodeSnippetFilter(SearchFilterSet):
    """Filter class for the CodeSnippet model."""

    search_fields = ("name", "code", "description")
    user = django_filters.ModelChoiceFilter(
        field_name="author",  # placeholder
        queryset=User.objects.all(),
        method="filter_user",
        label="User",
    )
    language = django_filters.ChoiceFilter(choices=LANGUAGES_CHOICES)
    confidence = django_filters.ChoiceFilter(choices=CONFIDENCE_CHOICES)
    validation_status = django_filters.ChoiceFilter(choices=VALIDATION_CHOICES)
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
        model = CodeSnippet
        fields = (
            "user",
            "language",
            "confidence",
            "validation_status",
            "updated_at__gte",
            "updated_at__lte",
        )

    def filter_user(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(author=value) | Q(contributors=value)
        ).distinct()
    

#############################################################################
# FQDN
#############################################################################


class FQDNFilter(SearchFilterSet):
    """Filter class for the FQDN model."""

    search_fields = ("fqdn", "description")
    user = django_filters.ModelChoiceFilter(
        field_name="author",  # placeholder
        queryset=User.objects.all(),
        method="filter_user",
        label="User",
    )
    confidence = django_filters.ChoiceFilter(choices=CONFIDENCE_CHOICES)
    validation_status = django_filters.ChoiceFilter(choices=VALIDATION_CHOICES)
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
        model = FQDN
        fields = (
            "user",
            "confidence",
            "validation_status",
            "updated_at__gte",
            "updated_at__lte",
        )

    def filter_user(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(author=value) | Q(contributors=value)
        ).distinct()
    

#############################################################################
# Hash
#############################################################################


class HashFilter(SearchFilterSet):
    """Filter class for the Hash model."""

    search_fields = ("filename", "url", "description", "md5", "sha1", "sha256", "url")
    user = django_filters.ModelChoiceFilter(
        field_name="author",  # placeholder
        queryset=User.objects.all(),
        method="filter_user",
        label="User",
    )
    platform = django_filters.ChoiceFilter(choices=PLATFORM_CHOICES)
    confidence = django_filters.ChoiceFilter(choices=CONFIDENCE_CHOICES)
    validation_status = django_filters.ChoiceFilter(choices=VALIDATION_CHOICES)
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
        model = FQDN
        fields = (
            "user",
            "platform",
            "confidence",
            "validation_status",
            "updated_at__gte",
            "updated_at__lte",
        )

    def filter_user(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(author=value) | Q(contributors=value)
        ).distinct()
    

#############################################################################
# IpAdd
#############################################################################


class IpAddFilter(SearchFilterSet):
    """Filter class for the IpAdd model."""

    search_fields = ("ip_address", "description")
    user = django_filters.ModelChoiceFilter(
        field_name="author",  # placeholder
        queryset=User.objects.all(),
        method="filter_user",
        label="User",
    )
    confidence = django_filters.ChoiceFilter(choices=CONFIDENCE_CHOICES)
    validation_status = django_filters.ChoiceFilter(choices=VALIDATION_CHOICES)
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
        model = IpAdd
        fields = (
            "user",
            "confidence",
            "validation_status",
            "updated_at__gte",
            "updated_at__lte",
        )

    def filter_user(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(author=value) | Q(contributors=value)
        ).distinct()
    

#############################################################################
# Vuln
#############################################################################

