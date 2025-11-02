from rest_framework.permissions import BasePermission


class UserPermissionPolicy:
    """UI and DRF (API) permisson policy for User objects."""

    def can(self, user, method, target_user=None):
        """Defines what the requesting user can do based on their role and HTTP method."""
        
        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest users are not allowed to do anything
            return None

        # === COMMON RULES ===
        if not target_user:
            # Without target user, any method is safe
            return True

        # === ADMIN RULES ===
        if user.is_superuser:
            # Admin can do everything except delete themselves
            if target_user and target_user.id == user.id and method == "DELETE":
                return False
            return True

        if method == "POST" and not user.is_superuser:
            # Only admins can create new users
            return False

        # === STAFF RULES ===
        if user.is_staff:
            if target_user:
                if target_user.id == user.id:
                    # Staff users can do anything on their own profile
                    return True
                if target_user.is_superuser or target_user.is_staff:
                    # Staff users cannot modify/delete other staffs/admins
                    return method in ("GET", "HEAD", "OPTIONS")
            return True

        # === STANDARD USER RULES ===
        if target_user.id == user.id:
            # Standard users can do anything on their own profile
            return True
        # Standard users cannot modify/delete other staffs/admins/users
        return method in ("GET", "HEAD", "OPTIONS")


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
