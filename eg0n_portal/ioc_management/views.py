"""Views for IoC Management app."""


from django.views.generic import TemplateView
from django.db.models import Count, Q
import django_tables2 as tables
from ioc_management.filters import EventFilter, VulnFilter, IpAddFilter, CodeSnippetFilter, FQDNFilter, HashFilter
from ioc_management.forms import EventForm, CodeSnippetForm, FQDNForm, IpAddForm, HashForm, VulnForm
from ioc_management.models import CodeSnippet, Event, FQDN, Hash, IpAdd, Vuln
from ioc_management.permissions import (
    CodeSnippetPermissionPolicy,
    EventPermissionPolicy,
    FQDNPermissionPolicy,
    HashPermissionPolicy,
    HomePermissionPolicy,
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
    OwnedEventHomeTable,
    ContributedEventHomeTable,
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
    TemplateMixin,
)


#############################################################################
# Generic Attribute
#############################################################################


class DuplicateQueryMixin:
    """Generic mixin to add a duplicated_exist context record."""

    def get_context_data(self, **kwargs):
        """Add attributes  to context."""
        context = super().get_context_data(**kwargs)
        model_class = self.model
        duplicated = False

        dup_q = Q()
        for field in self.duplicated_fields:
            dup_values = (
                model_class.objects.values(field)
                .annotate(c=Count("id"))
                .filter(c__gt=1)
                .values_list(field, flat=True)
            )
            if dup_values:
                dup_q |= Q(**{f"{field}__in": dup_values})
                duplicated = True
                break

        context["duplicated"] = duplicated
        return context


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
        # TODO
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
        qs = Event.objects.all().prefetch_related("contributors")
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

    # Fields rendered in the template
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

    filterset_class = CodeSnippetFilter
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

    # Fields rendered in the template
    template_name = "codesnippet_detail.html"


class CodeSnippetListView(CodeSnippetQueryMixin, ObjectListView):
    """HTML view for displaying a table of CodeSnippet objects."""

    pass


#############################################################################
# FQDN
#############################################################################


class FQDNQueryMixin:
    """Mixin encapsulating common queryset and permission logic for FQDN objects."""

    filterset_class = FQDNFilter
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


class FQDNDetailView(DuplicateQueryMixin, FQDNQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a FQDN."""

    # Fields rendered in the template
    template_name = "fqdn_detail.html"
    duplicated_fields = ["fqdn"]


class FQDNListView(FQDNQueryMixin, ObjectListView):
    """HTML view for displaying a table of FQDN objects."""

    pass


#############################################################################
# Hash
#############################################################################


class HashQueryMixin:
    """Mixin encapsulating common queryset and permission logic for Hash objects."""

    filterset_class = HashFilter
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


class HashDetailView(DuplicateQueryMixin, HashQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a Hash."""

    # Fields rendered in the template
    template_name = "hash_detail.html"
    duplicated_fields = ["md5", "sha1", "sha256", "filename"]


class HashListView(HashQueryMixin, ObjectListView):
    """HTML view for displaying a table of Hash objects."""

    pass


#############################################################################
# IpAdd
#############################################################################


class IpAddQueryMixin:
    """Mixin encapsulating common queryset and permission logic for IpAdd objects."""

    filterset_class = IpAddFilter
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


class IpAddDetailView(DuplicateQueryMixin, IpAddQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a IpAdd."""

    # Fields rendered in the template
    template_name = "ipadd_detail.html"
    duplicated_fields = ["ip_address"]


class IpAddListView(IpAddQueryMixin, ObjectListView):
    """HTML view for displaying a table of IpAdd objects."""

    pass


#############################################################################
# Vuln
#############################################################################


class VulnQueryMixin:
    """Mixin encapsulating common queryset and permission logic for Vuln objects."""

    filterset_class = VulnFilter
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


class VulnDetailView(DuplicateQueryMixin, VulnQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a Vuln."""

    # Fields rendered in the template
    template_name = "vuln_detail.html"
    duplicated_fields = ["cve"]


class VulnListView(VulnQueryMixin, ObjectListView):
    """HTML view for displaying a table of Vuln objects."""

    pass


#############################################################################
# Home
#############################################################################


class HomeView(TemplateMixin, TemplateView):
    """Render the home page."""

    policy_class = HomePermissionPolicy
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        """Add attributes  to context."""
        context = super().get_context_data(**kwargs)
        user_obj = self.request.user

        # Owned Event table
        owned_event_qs = Event.objects.filter(author=user_obj).order_by("-updated_at")
        owned_event_table = OwnedEventHomeTable(owned_event_qs)
        tables.RequestConfig(self.request, paginate=False).configure(owned_event_table)
        context["owned_event_table"] = owned_event_table

        # Contributed Event table
        contributed_event_qs = Event.objects.filter(contributors=user_obj).order_by("-updated_at")
        contributed_event_table = ContributedEventHomeTable(contributed_event_qs)
        tables.RequestConfig(self.request, paginate=False).configure(contributed_event_table)
        context["contributed_event_table"] = contributed_event_table

        return context
