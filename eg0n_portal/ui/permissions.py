from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission

class UserPermissionPolicy:
    """
    Centralized permission policy for users.
    Can be reused by both Django CBVs and DRF.
    """

    def can(self, user, method, target_user=None):
        """
        Defines what the requesting user can do based on their role and HTTP method.
        - user: the requesting user (request.user)
        - method: HTTP method (GET, POST, DELETE, etc.)
        - target_user: the user object being acted upon (for detail routes)
        """
        if not user.is_authenticated:
            return False

        method = method.upper()

        # === ADMIN RULES ===
        if user.is_superuser:
            # Admin can do everything...
            # ...except delete themselves
            if method == "DELETE" and target_user and target_user.id == user.id:
                return False
            return True

        # === STAFF RULES ===
        if user.is_staff:
            if target_user:
                # Can only act on users who share at least one group
                same_group = self._share_group(user, target_user)
                if not same_group:
                    return False

                # Cannot delete an admin
                if method == "DELETE" and target_user.is_superuser:
                    return False

                # All other operations are allowed
                return True
            else:
                # GET list allowed — staff sees only users sharing at least one group
                return method in ("GET", "HEAD", "OPTIONS")

        # === STANDARD USER RULES ===
        if not user.is_staff and not user.is_superuser:
            if target_user:
                # Can fully manage their own profile
                if target_user.id == user.id:
                    return True
                # Can only *view* other users that share a group
                if method in ("GET", "HEAD", "OPTIONS"):
                    return self._share_group(user, target_user)
                return False
            else:
                # For GET list: can view only users sharing a group
                return method in ("GET", "HEAD", "OPTIONS")

        return False

    def _share_group(self, user_a, user_b):
        """Helper: return True if two users share at least one group."""
        groups_a = set(user_a.groups.values_list("id", flat=True))
        groups_b = set(user_b.groups.values_list("id", flat=True))
        return len(groups_a & groups_b) > 0

class UserPermission(BasePermission):
    """
    DRF permission class using the shared UserPermissionPolicy.
    """

    def __init__(self):
        self.policy = UserPermissionPolicy()

    def has_permission(self, request, view):
        """
        Called before accessing the queryset.
        Used for list/create endpoints (no specific target object yet).
        """
        user = request.user
        method = request.method
        return self.policy.can(user, method, None)

    def has_object_permission(self, request, view, obj):
        """
        Called for detail routes or single-object operations.
        """
        user = request.user
        method = request.method
        return self.policy.can(user, method, obj)
    