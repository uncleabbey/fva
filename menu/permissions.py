from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import Vendor, Customer, User


class IsOwnerOrReadOnly(BasePermission):
  message = 'You must be the owner to perform this operation'
  

  def has_object_permission(self, request, view, obj):
    if request.method in SAFE_METHODS:
      return True
    return obj.vendorId.email == request.user.email

class IsVendorOrReadOnly(BasePermission):
  message = 'Only a Vendor can perform this operation'

  def has_permission(self, request, view):
    if request.method in SAFE_METHODS:
      return True
    user = request.user
    if user.isVendor:
      return True
    return False
