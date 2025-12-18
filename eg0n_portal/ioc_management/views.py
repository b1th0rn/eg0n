"""Views for Instance app."""

from ioc_management.filters import InstanceFilter
from ioc_management.forms import InstanceForm
from ioc_management.models import Instance
from ioc_management.permissions import InstancePermissionPolicy
from ioc_management.serializers import InstanceSerializer
from ioc_management.tables import InstanceTable
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

    pass


class InstanceListView(InstanceQueryMixin, ObjectListView):
    """HTML view for displaying a table of Instance objects."""

    pass
