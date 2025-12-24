"""Views for IoC Management app."""

import django_tables2 as tables
from ioc_management.filters import EventFilter
from ioc_management.forms import EventForm, CodeSnippetForm, FQDNForm, IpAddForm, HashForm, VulnForm
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
    CodeSnippetEmbeddedTable,
    CodeSnippetTable,
    EventTable,
    FQDNEmbeddedTable,
    FQDNTable,
    HashEmbeddedTable,
    HashTable,
    IpAddEmbeddedTable,
    IpAddTable,
    VulnEmbeddedTable,
    VulnTable,
)
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
# Generic Attribute
#############################################################################

class AttributeQueryMixin:
    """Standard actions for generic attributes."""

    def perform_create(self, serializer):
        """Set user and update event when creating a new attribute via REST API."""
        obj = serializer.save(author=self.request.user)
        obj.event.save()

    def perform_update(self, serializer):
        """Set contributed users and update event when creating a new CodeSnippet."""
        print("UPDATE")
        # serializer.save(last_editor=self.request.user)

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

    def perform_create(self, serializer):
        """Set user when creating a new Event."""
        serializer.save(author=self.request.user)


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

    def get_context_data(self, **kwargs):
        """Add attributes  to context."""
        context = super().get_context_data(**kwargs)
        event_obj = self.object

        # CodeSnippet table
        codesnippet_qs = event_obj.codesnippets.all().order_by("-updated_at")
        codesnippet_table = CodeSnippetEmbeddedTable(codesnippet_qs)
        tables.RequestConfig(self.request, paginate=False).configure(codesnippet_table)
        context["codesnippet_table"] = codesnippet_table

        # FQDN table
        fqdn_qs = event_obj.fqdns.all().order_by("-updated_at")
        fqdn_table = FQDNEmbeddedTable(fqdn_qs)
        tables.RequestConfig(self.request, paginate=False).configure(fqdn_table)
        context["fqdn_table"] = fqdn_table

        # Hash table
        hash_qs = event_obj.hashes.all().order_by("-updated_at")
        hash_table = HashEmbeddedTable(hash_qs)
        tables.RequestConfig(self.request, paginate=False).configure(hash_table)
        context["hash_table"] = hash_table

        # IpAdd table
        ipadd_qs = event_obj.ipadds.all().order_by("-updated_at")
        ipadd_table = IpAddEmbeddedTable(ipadd_qs)
        tables.RequestConfig(self.request, paginate=False).configure(ipadd_table)
        context["ipadd_table"] = ipadd_table

        # Vuln table
        vuln_qs = event_obj.vulns.all().order_by("-updated_at")
        vuln_table = VulnEmbeddedTable(vuln_qs)
        tables.RequestConfig(self.request, paginate=False).configure(vuln_table)
        context["vuln_table"] = vuln_table

        return context

class EventListView(EventQueryMixin, ObjectListView):
    """HTML view for displaying a table of Event objects."""

    pass


#############################################################################
# CodeSnippet
#############################################################################


class CodeSnippetQueryMixin:
    """Mixin encapsulating common queryset and permission logic for CodeSnippet objects."""

    filterset_class = None
    form_class = CodeSnippetForm
    model = CodeSnippet
    policy_class = CodeSnippetPermissionPolicy
    serializer_class = CodeSnippetSerializer
    table_class = CodeSnippetTable

    def get_queryset(self):
        """Return the queryset of CodeSnippet objects accessible to the current user."""
        qs = CodeSnippet.objects.all()
        return qs


class CodeSnippetAPIViewSet(CodeSnippetQueryMixin, AttributeQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the CodeSnippet model."""

    pass

class CodeSnippetChangeView(CodeSnippetQueryMixin, ObjectChangeView):
    """HTML view for updating an existing CodeSnippet."""

    pass


class CodeSnippetDeleteView(CodeSnippetQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single CodeSnippet."""

    pass


class CodeSnippetDetailView(CodeSnippetQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a CodeSnippet."""

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
    form_class = FQDNForm
    model = FQDN
    policy_class = FQDNPermissionPolicy
    serializer_class = FQDNSerializer
    table_class = FQDNTable

    def get_queryset(self):
        """Return the queryset of FQDN objects accessible to the current user."""
        qs = FQDN.objects.all()
        return qs


class FQDNAPIViewSet(FQDNQueryMixin, AttributeQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the FQDN model."""

    pass


class FQDNChangeView(FQDNQueryMixin, ObjectChangeView):
    """HTML view for updating an existing FQDN."""

    pass


class FQDNDeleteView(FQDNQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single FQDN."""

    pass


class FQDNDetailView(FQDNQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a FQDN."""

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
    form_class = HashForm
    model = Hash
    policy_class = HashPermissionPolicy
    serializer_class = HashSerializer
    table_class = HashTable

    def get_queryset(self):
        """Return the queryset of Hash objects accessible to the current user."""
        qs = Hash.objects.all()
        return qs


class HashAPIViewSet(HashQueryMixin, AttributeQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the Hash model."""

    pass

class HashChangeView(HashQueryMixin, ObjectChangeView):
    """HTML view for updating an existing Hash."""

    pass


class HashDeleteView(HashQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single Hash."""

    pass


class HashDetailView(HashQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a Hash."""

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
    form_class = IpAddForm
    model = IpAdd
    policy_class = IpAddPermissionPolicy
    serializer_class = IpAddSerializer
    table_class = IpAddTable

    def get_queryset(self):
        """Return the queryset of IpAdd objects accessible to the current user."""
        qs = IpAdd.objects.all()
        return qs


class IpAddAPIViewSet(IpAddQueryMixin, AttributeQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the IpAdd model."""

    pass


class IpAddChangeView(IpAddQueryMixin, ObjectChangeView):
    """HTML view for updating an existing IpAdd."""

    pass


class IpAddDeleteView(IpAddQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single IpAdd."""

    pass


class IpAddDetailView(IpAddQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a IpAdd."""

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
    form_class = VulnForm
    model = Vuln
    policy_class = VulnPermissionPolicy
    serializer_class = VulnSerializer
    table_class = VulnTable

    def get_queryset(self):
        """Return the queryset of Vuln objects accessible to the current user."""
        qs = Vuln.objects.all()
        return qs


class VulnAPIViewSet(VulnQueryMixin, AttributeQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the Vuln model."""

    pass


class VulnChangeView(VulnQueryMixin, ObjectChangeView):
    """HTML view for updating an existing Vuln."""

    pass


class VulnDeleteView(VulnQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single Vuln."""

    pass


class VulnDetailView(VulnQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a Vuln."""

    pass


class VulnListView(VulnQueryMixin, ObjectListView):
    """HTML view for displaying a table of Vuln objects."""

    pass
