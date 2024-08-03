from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )


class IsOwnerBasePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(obj, 'owner') and obj.owner == request.user or hasattr(obj, 'shop') and obj.shop == request.user
