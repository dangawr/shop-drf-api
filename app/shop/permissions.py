from rest_framework import permissions


class IsAuthenticatedOrStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if obj.cart.user == request.user:
            return True
        return request.user.is_staff


class IsStaffOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
