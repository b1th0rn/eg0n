"""Views for Instance app."""

import django_tables2 as tables
from ioc_management.filters import EventFilter
from ioc_management.forms import EventForm
from ioc_management.models import Event
from ioc_management.permissions import EventPermissionPolicy
from ioc_management.serializers import EventSerializer
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

class EventListView(EventQueryMixin, ObjectListView):
    """HTML view for displaying a table of Event objects."""

    pass
