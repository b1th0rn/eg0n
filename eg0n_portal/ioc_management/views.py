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
from ioc_management.tables import (
    EventTable,
    CodeSnippetTable,
    FQDNTable,
    HashTable,
    IpAddTable,
    VulnTable,
)
from ui.include.views import (
    APICRUDViewSet,
    APIRViewSet,
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

    filterset_class = None
    form_class = None
    model = CodeSnippet
    policy_class = CodeSnippetPermissionPolicy
    serializer_class = CodeSnippetSerializer
    table_class = CodeSnippetTable

    def get_queryset(self):
        """Return the queryset of CodeSnippet objects accessible to the current user."""
        qs = CodeSnippet.objects.all()
        return qs


class CodeSnippetAPIViewSet(CodeSnippetQueryMixin, APIRViewSet):
    """REST API ViewSet for the CodeSnippet model."""

    pass


class CodeSnippetListView(CodeSnippetQueryMixin, ObjectListView):
    """HTML view for displaying a table of CodeSnippet objects."""

    pass


#############################################################################
# FQDN
#############################################################################


class FQDNQueryMixin:
    """Mixin encapsulating common queryset and permission logic for FQDN objects."""

    filterset_class = None
    form_class = None
    model = FQDN
    policy_class = FQDNPermissionPolicy
    serializer_class = FQDNSerializer
    table_class = FQDNTable

    def get_queryset(self):
        """Return the queryset of FQDN objects accessible to the current user."""
        qs = FQDN.objects.all()
        return qs


class FQDNAPIViewSet(CodeSnippetQueryMixin, APIRViewSet):
    """REST API ViewSet for the FQDN model."""

    pass


class FQDNListView(FQDNQueryMixin, ObjectListView):
    """HTML view for displaying a table of FQDN objects."""

    pass


#############################################################################
# Hash
#############################################################################


class HashQueryMixin:
    """Mixin encapsulating common queryset and permission logic for Hash objects."""

    filterset_class = None
    form_class = None
    model = Hash
    policy_class = HashPermissionPolicy
    serializer_class = HashSerializer
    table_class = HashTable

    def get_queryset(self):
        """Return the queryset of Hash objects accessible to the current user."""
        qs = Hash.objects.all()
        return qs


class HashAPIViewSet(HashQueryMixin, APIRViewSet):
    """REST API ViewSet for the Hash model."""

    pass


class HashListView(HashQueryMixin, ObjectListView):
    """HTML view for displaying a table of Hash objects."""

    pass


#############################################################################
# IpAdd
#############################################################################


class IpAddQueryMixin:
    """Mixin encapsulating common queryset and permission logic for IpAdd objects."""

    filterset_class = None
    form_class = None
    model = IpAdd
    policy_class = IpAddPermissionPolicy
    serializer_class = IpAddSerializer
    table_class = IpAddTable

    def get_queryset(self):
        """Return the queryset of IpAdd objects accessible to the current user."""
        qs = IpAdd.objects.all()
        return qs


class IpAddAPIViewSet(IpAddQueryMixin, APIRViewSet):
    """REST API ViewSet for the IpAdd model."""

    pass


class IpAddListView(IpAddQueryMixin, ObjectListView):
    """HTML view for displaying a table of IpAdd objects."""

    pass


#############################################################################
# Vuln
#############################################################################


class VulnQueryMixin:
    """Mixin encapsulating common queryset and permission logic for Vuln objects."""

    filterset_class = None
    form_class = None
    model = Vuln
    policy_class = VulnPermissionPolicy
    serializer_class = VulnSerializer
    table_class = VulnTable

    def get_queryset(self):
        """Return the queryset of Vuln objects accessible to the current user."""
        qs = Vuln.objects.all()
        return qs


class VulnAPIViewSet(VulnQueryMixin, APIRViewSet):
    """REST API ViewSet for the Vuln model."""

    pass


class VulnListView(VulnQueryMixin, ObjectListView):
    """HTML view for displaying a table of Vuln objects."""

    pass
