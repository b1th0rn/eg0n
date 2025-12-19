"""Views for Instance app."""

import django_tables2 as tables
from ioc_management.filters import EventFilter, InstanceFilter
from ioc_management.forms import EventForm, InstanceForm
from ioc_management.models import Event, Instance
from ioc_management.permissions import EventPermissionPolicy, InstancePermissionPolicy
from ioc_management.serializers import EventSerializer, InstanceSerializer
from ioc_management.tables import EventTable, InstanceTable
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
# Instance
#############################################################################


class InstanceQueryMixin:
    """Mixin encapsulating common queryset and permission logic for Instance objects."""

    filterset_class = InstanceFilter
    form_class = InstanceForm
    model = Instance
    policy_class = InstancePermissionPolicy
    serializer_class = InstanceSerializer
    table_class = InstanceTable

    def get_queryset(self):
        """Return the queryset of Instance objects accessible to the current user."""
        qs = Instance.objects.all()
        return qs


class InstanceAPIViewSet(InstanceQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the Instance model."""

    pass


class InstanceBulkDeleteView(InstanceQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple Instance objects at once."""

    pass


class InstanceChangeView(InstanceQueryMixin, ObjectChangeView):
    """HTML view for updating an existing Instance."""

    pass


class InstanceCreateView(InstanceQueryMixin, ObjectCreateView):
    """HTML view for creating a new Instance."""

    pass


class InstanceDeleteView(InstanceQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single Instance."""

    pass


class InstanceDetailView(InstanceQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a Instance."""


    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")
    # exclude = ("id",)
    sequence = ("id", "name", "created_at", "updated_at")

class InstanceListView(InstanceQueryMixin, ObjectListView):
    """HTML view for displaying a table of Instance objects."""

    pass


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


    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")
    exclude = ("id",)
    sequence = ("name", "created_at", "updated_at")

class EventListView(EventQueryMixin, ObjectListView):
    """HTML view for displaying a table of Event objects."""

    pass
