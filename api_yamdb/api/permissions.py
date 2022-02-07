from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):
    """Проверка роли администартора."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_administrator) or request.user.is_superuser


class IsModerator(permissions.BasePermission):
    """Проверка роли модератора."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator


class IsAdministratorOrReadOnly(permissions.BasePermission):
    """Проверка роли администартора."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_administrator
            or request.method in permissions.SAFE_METHODS
        )


class AuthorStaffOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in 'GET'
            or request.user.is_moderator or request.user.is_administrator
            or request.user == obj.author
        )
