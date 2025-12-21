"""Views for IoC Management app."""

import django_tables2 as tables
from ioc_management.filters import EventFilter
from ioc_management.forms import EventForm
from ioc_management.models import CodeSnippet, Event, FQDN, Hash, IpAdd, Vuln
from ioc_management.permissions import (
    CodeSnippetPermissionPolicy,
    EventPermissionPolicy,
    FQDNPermissionPolicy,
    HashPermissionPolicy,
    IpAddPermissionPolicy,
    VulnPermissionPolicy,
)
from ioc_management.serializers import (
    CodeSnippetSerializer,
    EventSerializer,
    FQDNSerializer,
    HashSerializer,
    IpAddSerializer,
    VulnSerializer,
)
from ioc_management.tables import EventTable
from ui.include.views import (
    APICRUDViewSet,
    ObjectBulkDeleteView,
    ObjectChangeView,
    ObjectCreateView,
    ObjectDeleteView,
    ObjectDetailView,
    ObjectListView,
)


#############################################################################
# Event
#############################################################################


class EventQueryMixin:
    """Mixin encapsulating common queryset and permission logic for Event objects."""

    filterset_class = EventFilter
    form_class = EventForm
    model = Event
    policy_class = EventPermissionPolicy
    serializer_class = EventSerializer
    table_class = EventTable

    def get_queryset(self):
        """Return the queryset of Event objects accessible to the current user."""
        qs = Event.objects.all()
        return qs


class EventAPIViewSet(EventQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the Event model."""

    pass


class EventBulkDeleteView(EventQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple Event objects at once."""

    pass


class EventChangeView(EventQueryMixin, ObjectChangeView):
    """HTML view for updating an existing Event."""

    pass


class EventCreateView(EventQueryMixin, ObjectCreateView):
    """HTML view for creating a new Event."""

    pass


class EventDeleteView(EventQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single Event."""

    pass


class EventDetailView(EventQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a Event."""

    author = tables.LinkColumn("user_detail", args=[tables.A("author__pk")])
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")
    exclude = ("id",)
    sequence = ("name", "created_at", "updated_at")
    template_name = "event_detail.html"


class EventListView(EventQueryMixin, ObjectListView):
    """HTML view for displaying a table of Event objects."""

    pass


#############################################################################
# CodeSnippet
#############################################################################


class CodeSnippetQueryMixin:
    """Mixin encapsulating common queryset and permission logic for CodeSnippet objects."""

    filterset_class = None  # API only
    form_class = None  # API only
    model = CodeSnippet
    policy_class = CodeSnippetPermissionPolicy
    serializer_class = CodeSnippetSerializer
    table_class = None  # API only

    def get_queryset(self):
        """Return the queryset of CodeSnippet objects accessible to the current user."""
        qs = CodeSnippet.objects.all()
        return qs


class CodeSnippetAPIViewSet(CodeSnippetQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the CodeSnippet model."""

    pass


#############################################################################
# FQDN
#############################################################################


class FQDNQueryMixin:
    """Mixin encapsulating common queryset and permission logic for FQDN objects."""

    filterset_class = None  # API only
    form_class = None  # API only
    model = FQDN
    policy_class = FQDNPermissionPolicy
    serializer_class = FQDNSerializer
    table_class = None  # API only

    def get_queryset(self):
        """Return the queryset of FQDN objects accessible to the current user."""
        qs = FQDN.objects.all()
        return qs


class FQDNAPIViewSet(CodeSnippetQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the FQDN model."""

    pass


#############################################################################
# Hash
#############################################################################


class HashQueryMixin:
    """Mixin encapsulating common queryset and permission logic for Hash objects."""

    filterset_class = None  # API only
    form_class = None  # API only
    model = Hash
    policy_class = HashPermissionPolicy
    serializer_class = HashSerializer
    table_class = None  # API only

    def get_queryset(self):
        """Return the queryset of Hash objects accessible to the current user."""
        qs = Hash.objects.all()
        return qs


class HashAPIViewSet(HashQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the Hash model."""

    pass


#############################################################################
# IpAdd
#############################################################################


class IpAddQueryMixin:
    """Mixin encapsulating common queryset and permission logic for IpAdd objects."""

    filterset_class = None  # API only
    form_class = None  # API only
    model = IpAdd
    policy_class = IpAddPermissionPolicy
    serializer_class = IpAddSerializer
    table_class = None  # API only

    def get_queryset(self):
        """Return the queryset of IpAdd objects accessible to the current user."""
        qs = IpAdd.objects.all()
        return qs


class IpAddAPIViewSet(IpAddQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the IpAdd model."""

    pass


#############################################################################
# Vuln
#############################################################################


class VulnQueryMixin:
    """Mixin encapsulating common queryset and permission logic for Vuln objects."""

    filterset_class = None  # API only
    form_class = None  # API only
    model = Vuln
    policy_class = VulnPermissionPolicy
    serializer_class = VulnSerializer
    table_class = None  # API only

    def get_queryset(self):
        """Return the queryset of Vuln objects accessible to the current user."""
        qs = Vuln.objects.all()
        return qs


class VulnAPIViewSet(VulnQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the Vuln model."""

    pass
