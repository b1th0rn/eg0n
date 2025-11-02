"""Views for managing Groups.

This module provides both HTML UI views and REST API endpoints
for the `Group` model, including creation, modification,
retrieval, and deletion.
"""

from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib import messages as django_msgs
from django.contrib.auth.models import Group, User
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from constance import config
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from ui.include import messages
from ui.permissions import UserPermissionPolicy, UserPermission
from ui.include.permissions import IsAdmin
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
from ui.filters import GroupFilter, TokenFilter, UserFilter
from ui.forms import GroupForm, UserForm
from ui.serializers import GroupSerializer, UserSerializer
from ui.tables import GroupTable, TokenTable, UserTable


#############################################################################
# Contance settings
#############################################################################


class ConstanceListView(TemplateView):
    """
    View to display Constance settings as a list.

    Inherits from:
        CommonMixin
        TemplateView
    """

    permission_classes = [IsAdmin]
    template_name = "ui/settings_list.html"

    def get_variables(self):
        """
        Retrieve all Constance configuration variables.

        Returns:
            dict: A dictionary with variable names as keys and their values from the Constance config.
        """
        return {key: getattr(config, key) for key in dir(config)}

    def get_context_data(self, **kwargs):
        """
        Add Constance variables to the template context.

        Returns:
            dict: Template context including Constance variables under the 'variables' key.
        """
        context = super().get_context_data(**kwargs)
        context["variables"] = self.get_variables()
        return context


class ConstanceUpdateView(TemplateView):
    """
    View to display and update Constance settings via a form.

    Inherits from:
        CommonMixin
        TemplateView
    """

    template_name = "ui/settings_form.html"
    permission_classes = [IsAdmin]

    def get_variables(self):
        """
        Retrieve all Constance configuration variables.

        Returns:
            dict: A dictionary with variable names as keys and their values from the Constance config.
        """
        return {key: getattr(config, key) for key in dir(config)}

    def get(self, request, *args, **kwargs):
        """
        Handle GET request and render the settings form with current values.

        Args:
            request (HttpRequest): The current HTTP request object.

        Returns:
            HttpResponse: Rendered template with context including all Constance variables.
        """
        context = self.get_context_data()
        context["variables"] = self.get_variables()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to update Constance settings.

        Iterates through POSTed variables, converts them to the correct type,
        updates the Constance backend, and displays success or error messages.

        Args:
            request (HttpRequest): The current HTTP request object.

        Returns:
            HttpResponseRedirect: Redirects to the settings list view after updating.
        """
        for key in dir(config):
            if key in request.POST:
                value = request.POST[key]
                default_value = getattr(config, key)
                # Convert type to match default
                if isinstance(default_value, bool):
                    value = value.lower() in ["true", "1", "on"]
                elif isinstance(default_value, int):
                    try:
                        value = int(value)
                    except ValueError:
                        django_msgs.error(
                            request, f"{messages.MSG_VALUE_ERROR} ({key})."
                        )
                        continue
                config._backend.set(key, value)
        django_msgs.success(request, messages.MSG_CONFIG_UPDATED)
        return redirect("settings_list")


#############################################################################
# Group
#############################################################################


class GroupQueryMixin:
    """Mixin encapsulating common queryset and permission logic for `Group`.

    Used by both HTML views and API views.
    """
    filterset_class = GroupFilter
    form_class = GroupForm
    model = Group
    serializer_class = GroupSerializer
    table_class = GroupTable


    def test_func(self):
        # Define who can GET/HEAD/OPTION/DELETE/PATCH/POST/PUT
        user = self.request.user
        method = self.request.method.upper()
        if method in ("GET", "HEAD", "OPTIONS"):
            return user.is_authenticated
        return user.is_authenticated and user.is_superuser

    def get_queryset(self):
        """Return the queryset of `Group` objects accessible to the current user.

        - Superusers can access all `Group` objects.
        - Non-superusers can only access `Group` objects they belong to.
        """
        qs = Group.objects.all()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `Group` objects
            return qs
        # Non-admin users can only see the `Group` objects they belong to
        return qs.filter(user=user)

    def get_object(self):
        """Return a `Group` object only if the user has permission.

        - Superusers can access any `Group`.
        - Non-superusers can only access `Group` objects they belong to.

        Raises:
            PermissionDenied: If the user does not have access.
        """
        obj = super().get_object()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `Group` objects
            return obj
        if user in obj.user_set.all():
            # Non-admin users can only see the `Group` objects they belong to
            return obj
        raise PermissionDenied(messages.PERMISSION_DENIED)


class GroupAPIViewSet(GroupQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the `Group` model."""
    pass


class GroupBulkDeleteView(GroupQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple `Group` objects at once."""
    pass


class GroupChangeView(GroupQueryMixin, ObjectChangeView):
    """HTML view for updating an existing `Group`."""
    pass


class GroupCreateView(GroupQueryMixin, ObjectCreateView):
    """HTML view for creating a new `Group`."""
    pass


class GroupDeleteView(GroupQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single `Group`."""
    pass


class GroupDetailView(GroupQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a `Group`."""
    exclude = ["id"]


class GroupListView(GroupQueryMixin, ObjectListView):
    """HTML view for displaying a table of `Group` objects."""
    pass

#############################################################################
# User
#############################################################################

"""
CBV:
as_view()
→ dispatch()
   → LoginRequiredMixin
   → UserPassesTestMixin → test_func()
→ get()
   → get_object() (di solito non riceve un queryset specifico)
      → get_queryset() (se personalizzo get_queryset, influenzo get_object)
   → get_context_data()
→ render_to_response()

TemplateView:
as_view()
→ dispatch()
   → (LoginRequiredMixin / UserPassesTestMixin controllano permessi)
→ get()
   → get_context_data()
→ render_to_response()

DRF (REST API):
as_view()
→ dispatch()
   → perform_authentication(request)
   → check_permissions(request)
   → get() / post() / put() / delete()
      → get_object() (solo per Detail)
        → get_queryset()
        → check_object_permissions(request, obj)
            has_object_permission su ogni class
      → serializer (serializzazione)
→ Response()
"""
class UserQueryMixin:
    """Mixin encapsulating common queryset and permission logic for `User`.

    Used by both HTML views and API views.
    """
    filterset_class = UserFilter
    form_class = UserForm
    model = User
    permission_classes = [UserPermission] # Required for API
    # policy = UserPermissionPolicy
    policy_class = UserPermissionPolicy
    serializer_class = UserSerializer
    table_class = UserTable


    # def test_func(self):
    #     """
    #     Called automatically by UserPassesTestMixin to determine access.
    #     """
    #     user = self.request.user
    #     method = self.request.method
    #     target_user = self.get_object()
    #     return self.policy.can(user, method, target_user)
    
    def get_queryset(self):
        """
        Limit visible users depending on the requester's role.
        """
        qs = User.objects.all().order_by("username")
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return qs
        # Staff and standard users can see users who share at least one group
        groups = user.groups.all()
        return qs.filter(
            Q(groups__in=groups) | Q(id=user.id)
        ).distinct()


    # def get_object(self):
    #     """Return a `User` object only if the user has permission."""
    #     obj = super().get_object()
    #     if not self.get_queryset().filter(pk=obj.pk).exists():
    #         raise PermissionDenied(messages.PERMISSION_DENIED)
    #     return obj


class UserAPIViewSet(UserQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the `User` model."""
    pass

class UserBulkDeleteView(UserQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple `User` objects at once."""
    pass


class UserChangeView(UserQueryMixin, ObjectChangeView):
    """HTML view for updating an existing `User`."""
    pass


class UserCreateView(UserQueryMixin, ObjectCreateView):
    """HTML view for creating a new `User`."""
    pass


class UserDeleteView(UserQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single `User`."""
    pass


class UserDetailView(UserQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a `User`."""
    exclude = ["id", "password"]
    sequence = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_superuser",
        "is_staff",
    ]


class UserListView(UserQueryMixin, ObjectListView):
    """HTML view for displaying a table of `User` objects."""
    pass


#############################################################################
# Token
#############################################################################


class TokenQueryMixin:
    """Mixin encapsulating common queryset and permission logic for `Token`.

    Used by both HTML views and API views.
    """
    filterset_class = TokenFilter
    # form_class = None
    model = Token
    # serializer_class = None
    table_class = TokenTable

    def get_queryset(self):
        """Return the queryset of `User` objects accessible to the current user.

        - Superusers can access all `User` objects.
        - Staff users can see users who share at least one group
        - Non-superusers can only access their own `User` object.
        """
        qs = Token.objects.all()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return qs
        if user.is_staff:
            # Staff users can see users who share at least one group
            groups = user.groups.all()
            return qs.filter(user__groups__in=groups).distinct()
        # Non-admin users can only see their own user
        return qs.filter(user__username=user.username)

    def get_object(self):
        """Return a `User` object only if the user has permission.

        - Superusers can access any `User`.
        - Staff users can see users who share at least one group.
        - Non-superusers can only access their own `User` object.

        Raises:
            PermissionDenied: If the user does not have access.
        """
        obj = super().get_object()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return obj
        if user.is_staff:
            if obj.is_superuser:
                raise PermissionDenied(messages.PERMISSION_ADMIN)
            # Staff users can see users who share at least one group
            if user.groups.filter(
                pk__in=obj.groups.values_list("pk", flat=True)
            ).exists():
                return obj
        if user == obj:
            # Non-admin users can only see the `Group` objects they belong to
            return obj
        raise PermissionDenied(messages.PERMISSION_DENIED)


class TokenBulkDeleteView(TokenQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple `Token` objects at once."""
    pass


class TokenCreateView(TokenQueryMixin, ObtainAuthToken):
    """
    API per permettere a ciascun utente di generare il proprio token.
    """

    def post(self, request, *args, **kwargs):
        Token.objects.get_or_create(user=request.user)
        return redirect("token_list")


class TokenDeleteView(TokenQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single `Token`."""
    pass


class TokenListView(TokenQueryMixin, ObjectListView):
    """HTML view for displaying a table of `Token` objects."""
    pass


#############################################################################
# Home
#############################################################################

class HomePermissionPolicy:
    """
    Policy per TemplateView.
    """

    def can(self, user, method):
        """
        Restituisce:
        - True: ha permesso → mostra la view
        - False: utente autenticato ma senza permesso → 403
        - None: utente anonimo → 401 / redirect
        """
        if not user.is_authenticated:
            return None
        return True


class HomeView(TemplateMixin, TemplateView):
    """
    Render the home page for authenticated users.

    The template is loaded from: templates/ui
    """

    policy_class = HomePermissionPolicy
    template_name = "ui/home.html"
