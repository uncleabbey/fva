from rest_framework import serializers
from .models import Menu
from accounts.models import Vendor, Customer


class VendorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Vendor
    fields = ['id', 'email', 'phone_number', 'business_name']

class MenuSerializers(serializers.ModelSerializer):
  vendorId = VendorSerializer(read_only=True)
  class Meta:
    model = Menu
    fields = '__all__'
    depth = 1