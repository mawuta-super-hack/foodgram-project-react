from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка, что админ или суперюзер и безопасный метод"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_staff))


class IsAdminAuthorOrReadOnly(permissions.BasePermission):
    """Проверка авторизации и доступа к объектам"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff
                or obj.author == request.user)
