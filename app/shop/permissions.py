from rest_framework import permissions


class IsCartItemOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.cart.user == request.user:
            return True
