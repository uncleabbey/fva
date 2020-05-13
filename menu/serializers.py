from rest_framework import serializers
from .models import Menu
from accounts.models import Vendor, Customer, User


class VendorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Vendor
    fields = ['id', 'email', 'phone_number', 'business_name']

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'phone_number', 'isVendor']

class MenuSerializers(serializers.ModelSerializer):
  vendorId = UserSerializer(read_only=True)
  class Meta:
    model = Menu
    fields = '__all__'
    depth = 1