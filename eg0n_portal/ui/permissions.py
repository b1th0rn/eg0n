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

        if method == "POST" and not user.is_superuser:
            # Only admins can create new users
            return False
        
        # === ADMIN RULES ===
        if user.is_superuser:
            # Admin can do everything...
            # ...except delete themselves
            if target_user and target_user.id == user.id and method == "DELETE":
                return False
            return True

        # === STAFF RULES ===
        if user.is_staff:
            if target_user:
                if target_user.id == user.id:
                    return True
                if target_user.is_superuser or target_user.is_staff:
                    return method in ("GET", "HEAD", "OPTIONS")
            return True

        # === STANDARD USER RULES ===
        if target_user:
            if target_user.id == user.id:
                return True
            return method in ("GET", "HEAD", "OPTIONS")

        # Without target user, any method is safe
        return True


class UserPermission(BasePermission):
    """
    DRF permission class using the shared UserPermissionPolicy.
    """
    # policy_class = None

    # def __init__(self):
    #     self.policy = self.policy_class()

    def has_permission(self, request, view):
        """
        Called before accessing the queryset.
        Used for list/create endpoints (no specific target object yet).
        """
        policy_class = getattr(view, "policy_class", None)
        policy = policy_class()
        user = request.user
        method = request.method
        return policy.can(user, method, None)

    def has_object_permission(self, request, view, obj):
        """
        Called for detail routes or single-object operations.
        """
        policy_class = getattr(view, "policy_class", None)
        policy = policy_class()
        user = request.user
        method = request.method
        return policy.can(user, method, obj)
    