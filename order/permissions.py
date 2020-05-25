from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import Customer


class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner to perform this operation'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.customerId.email == request.user.email


class IsVendor(BasePermission):
    message = 'You must be the owner to perform this operation'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.isVendor:
            return True
        return False
