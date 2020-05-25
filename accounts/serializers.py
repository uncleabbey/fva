from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Vendor, Customer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'isVendor', 'isConfirmed']


class VendorCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, help_text="User email")
    phone_number = serializers.CharField(
        max_length=15, help_text="User phone number")
    business_name = serializers.CharField(
        max_length=50, help_text="Business Name")

    class Meta:
        model = Vendor
        fields = ['id', 'email', 'phone_number',
                  'business_name', 'unique_ref', 'create_date']

    def create(self, validated_data):
        return Vendor.objects.create_vendor(**validated_data)


class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, help_text="User email")
    phone_number = serializers.CharField(
        max_length=15, help_text="User phone number")
    first_name = serializers.CharField(
        max_length=50, help_text="First Name")
    last_name = serializers.CharField(
        max_length=50, help_text="Last Name")

    class Meta:
        model = Customer
        fields = ['id', 'email', 'phone_number',
                  'first_name', 'last_name', 'unique_ref', 'create_date']

    def create(self, validated_data):
        return Customer.objects.create_customer(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, help_text="User email")
    password = serializers.CharField(
        min_length=8, write_only=True, help_text="Password must be at least 8 characters")

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )

        try:
            userObj = Vendor.objects.get(email=user.email)
        except Vendor.DoesNotExist:
            userObj = None
        try:
            if userObj is None:
                userObj = Customer.objects.get(email=user.email)
        except Customer.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'email': user.email,
        }


class SetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=128, write_only=True, help_text="Password must be at least 8 characters")

    class Meta:
        model = User
        fields = ['password', 'unique_ref']
