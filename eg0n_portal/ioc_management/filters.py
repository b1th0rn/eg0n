"""Filter definitions for IoC Management app."""

from datetime import timedelta
from django import forms
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.utils import timezone
import django_filters
from ioc_management.models import Event, PLATFORM_CHOICES, LANGUAGES_CHOICES, VALIDATION_CHOICES, CONFIDENCE_CHOICES, CodeSnippet, Hash, IpAdd, FQDN, Vuln
from ui.include.filters import SearchFilterSet


CVSS_SEVERITY = [
    ("low", "Low (0.1 - 3.9)"),
    ("medium", "Medium (4.0 - 6.9)"),
    ("high", "High (7.0 - 8.9)"),
    ("critical", "Critical (9.0 - 10.0)"),
]

EXPIRATION_CHOICES = [
    ("expired", "Expired"),
    ("7d", "Expires within 7 days"),
    ("15d", "Expires within 15 days"),
    ("30d", "Expires within 30 days"),
    ("30d+", "Expires after 30 days"),
]


#############################################################################
# Generic Attribute
#############################################################################


class DuplicateFilterMixin:
    """Generic mixin to filter duplicated records on one or more fields."""

    def filter_duplicates(self, queryset, name, value):
        """Filters queryset to only include objects with duplicates."""
        if not value or not hasattr(self, "duplicated_fields"):
            return queryset

        combined_q = Q()
        for field in self.duplicated_fields:
            duplicated_values = (
                queryset.values(field)
                .annotate(count=Count("id"))
                .filter(count__gt=1)
                .values_list(field, flat=True)
            )
            combined_q |= Q(**{f"{field}__in": duplicated_values})

        return queryset.filter(combined_q).distinct()
    
class UserFilterMixin:
    def filter_user(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(author=value) | Q(contributors=value)
        ).distinct()
    
class ExpirationFilterMixin:
    def filter_expiration(self, queryset, name, value):
        today = timezone.now().date()

        if value == "expired":
            return queryset.filter(expired_at__lte=today)

        days_map = {
            "7d": 7,
            "15d": 15,
            "30d": 30,
        }

        if value in days_map:
            future_limit = today + timedelta(days=days_map[value])
            return queryset.filter(
                Q(expired_at__gte=today, expired_at__lte=future_limit)
            )

        if value == "30d+":
            future_limit = today + timedelta(days=30)
            return queryset.filter(expired_at__gt=future_limit)

        return queryset


#############################################################################
# Event
#############################################################################


class EventFilter(UserFilterMixin, SearchFilterSet):
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


#############################################################################
# CodeSnippet
#############################################################################


class CodeSnippetFilter(ExpirationFilterMixin, UserFilterMixin, SearchFilterSet):
    """Filter class for the CodeSnippet model."""

    search_fields = ("name", "code", "description")
    language = django_filters.ChoiceFilter(choices=LANGUAGES_CHOICES)
    confidence = django_filters.ChoiceFilter(choices=CONFIDENCE_CHOICES)
    validation_status = django_filters.ChoiceFilter(choices=VALIDATION_CHOICES)
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
    expiration = django_filters.ChoiceFilter(
        choices=EXPIRATION_CHOICES,
        method="filter_expiration",
        label="Expiration status",
    )

    class Meta:
        model = CodeSnippet
        fields = (
            "user",
            "language",
            "confidence",
            "validation_status",
            "expiration",
            "updated_at__gte",
            "updated_at__lte",
        )

    

#############################################################################
# FQDN
#############################################################################


class FQDNFilter(DuplicateFilterMixin, ExpirationFilterMixin, UserFilterMixin, SearchFilterSet):
    """Filter class for the FQDN model."""

    search_fields = ("fqdn", "description")
    user = django_filters.ModelChoiceFilter(
        field_name="author",  # placeholder
        queryset=User.objects.all(),
        method="filter_user",
        label="User",
    )
    expiration = django_filters.ChoiceFilter(
        choices=EXPIRATION_CHOICES,
        method="filter_expiration",
        label="Expiration status",
    )
    duplicates = django_filters.ChoiceFilter(
        method="filter_duplicates",
        label="Has duplicates",
        choices=[("1", "Yes")],
        widget=forms.Select,
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
    duplicated_fields = ["fqdn"]

    class Meta:
        model = FQDN
        fields = (
            "user",
            "confidence",
            "validation_status",
            "expiration",
            "duplicates",
            "updated_at__gte",
            "updated_at__lte",
        )


#############################################################################
# Hash
#############################################################################


class HashFilter(DuplicateFilterMixin, UserFilterMixin, ExpirationFilterMixin, SearchFilterSet):
    """Filter class for the Hash model."""

    search_fields = ("filename", "url", "description", "md5", "sha1", "sha256", "url")
    user = django_filters.ModelChoiceFilter(
        field_name="author",  # placeholder
        queryset=User.objects.all(),
        method="filter_user",
        label="User",
    )
    expiration = django_filters.ChoiceFilter(
        choices=EXPIRATION_CHOICES,
        method="filter_expiration",
        label="Expiration status",
    )
    duplicates = django_filters.ChoiceFilter(
        method="filter_duplicates",
        label="Has duplicates",
        choices=[("1", "Yes")],
        widget=forms.Select,
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
    duplicated_fields = ["md5", "sha1", "sha256", "filename"]

    class Meta:
        model = FQDN
        fields = (
            "user",
            "platform",
            "confidence",
            "validation_status",
            "expiration",
            "duplicates",
            "updated_at__gte",
            "updated_at__lte",
        )


#############################################################################
# IpAdd
#############################################################################


class IpAddFilter(DuplicateFilterMixin, ExpirationFilterMixin, UserFilterMixin, SearchFilterSet):
    """Filter class for the IpAdd model."""

    search_fields = ("ip_address", "description")
    user = django_filters.ModelChoiceFilter(
        field_name="author",  # placeholder
        queryset=User.objects.all(),
        method="filter_user",
        label="User",
    )
    expiration = django_filters.ChoiceFilter(
        choices=EXPIRATION_CHOICES,
        method="filter_expiration",
        label="Expiration status",
    )
    confidence = django_filters.ChoiceFilter(choices=CONFIDENCE_CHOICES)
    validation_status = django_filters.ChoiceFilter(choices=VALIDATION_CHOICES)
    duplicates = django_filters.ChoiceFilter(
        method="filter_duplicates",
        label="Has duplicates",
        choices=[("1", "Yes")],
        widget=forms.Select,
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
    duplicated_fields = ["ip_address"]

    class Meta:
        model = IpAdd
        fields = (
            "user",
            "confidence",
            "validation_status",
            "expiration",
            "duplicates",
            "updated_at__gte",
            "updated_at__lte",
        )
    
#############################################################################
# Vuln
#############################################################################


class VulnFilter(DuplicateFilterMixin, UserFilterMixin, SearchFilterSet):
    """Filter class for the Vuln model."""

    search_fields = ("name", "cve", "description", "exploitation_details")
    user = django_filters.ModelChoiceFilter(
        field_name="author",  # placeholder
        queryset=User.objects.all(),
        method="filter_user",
        label="User",
    )
    severity = django_filters.ChoiceFilter(
        choices=CVSS_SEVERITY,
        method="filter_severity",
        label="Severity",
    )
    duplicates = django_filters.ChoiceFilter(
        method="filter_duplicates",
        label="Has duplicates",
        choices=[("1", "Yes")],
        widget=forms.Select,
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
    duplicated_fields = ["cve"]

    class Meta:
        model = Vuln
        fields = (
            "user",
            "severity",
            "duplicates",
            "updated_at__gte",
            "updated_at__lte",
        )

    def filter_severity(self, queryset, name, value):
        if not value:
            return queryset

        ranges = {
            "low": Q(cvss__gte=0.1, cvss__lte=3.9),
            "medium": Q(cvss__gte=4.0, cvss__lte=6.9),
            "high": Q(cvss__gte=7.0, cvss__lte=8.9),
            "critical": Q(cvss__gte=9.0, cvss__lte=10.0),
        }

        return queryset.filter(ranges[value])
