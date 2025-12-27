"""Permissions for IoC Management app."""

#############################################################################
# Event
#############################################################################


class EventPermissionPolicy:
    """UI and DRF (API) permisson policy for Event objects."""

    def can(self, user, method, target=None, payload=None):
        """Defines what the requesting user can do based on their role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest users are not allowed to do anything
            return None

        # === COMMON RULES ===
        return True


#############################################################################
# CodeSnippet
#############################################################################


class CodeSnippetPermissionPolicy:
    """UI and DRF (API) permisson policy for CodeSnippet objects."""

    def can(self, user, method, target=None, payload=None):
        """Defines what the requesting user can do based on their role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest users are not allowed to do anything
            return None

        # === COMMON RULES ===
        return True
    

#############################################################################
# FQDN
#############################################################################


class FQDNPermissionPolicy:
    """UI and DRF (API) permisson policy for FQDN objects."""

    def can(self, user, method, target=None, payload=None):
        """Defines what the requesting user can do based on their role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest users are not allowed to do anything
            return None

        # === COMMON RULES ===
        return True
    

#############################################################################
# Hash
#############################################################################


class HashPermissionPolicy:
    """UI and DRF (API) permisson policy for Hash objects."""

    def can(self, user, method, target=None, payload=None):
        """Defines what the requesting user can do based on their role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest users are not allowed to do anything
            return None

        # === COMMON RULES ===
        return True


#############################################################################
# IpAdd
#############################################################################


class IpAddPermissionPolicy:
    """UI and DRF (API) permisson policy for IpAdd objects."""

    def can(self, user, method, target=None, payload=None):
        """Defines what the requesting user can do based on their role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest users are not allowed to do anything
            return None

        # === COMMON RULES ===
        return True
    

#############################################################################
# Vuln
#############################################################################


class VulnPermissionPolicy:
    """UI and DRF (API) permisson policy for Vuln objects."""

    def can(self, user, method, target=None, payload=None):
        """Defines what the requesting user can do based on their role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest users are not allowed to do anything
            return None

        # === COMMON RULES ===
        return True
    

#############################################################################
# Home
#############################################################################


class HomePermissionPolicy:
    """UI permisson policy for Home."""

    def can(self, user, method, target, payload):
        """Defines what the requesting user can do based on target, role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest access is denied
            return None

        # === COMMON RULES ===
        return True
