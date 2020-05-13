from django.shortcuts import render, get_object_or_404
from rest_framework import views, generics, permissions, status
from rest_framework.response import Response
from .serializers import CustomerSerializer, VendorSerializer, LoginSerializer
from knox.models import AuthToken
from .models import User

class VendorRegView(generics.CreateAPIView):
    
  serializer_class = VendorSerializer

  def post(self, request):
        """
        create:
          Create a new vendor.
        """  
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token =  AuthToken.objects.create(user)[1]
        return Response({
          "message": "Vendor created succesfully",
          'vendor': serializer.data,
          'token': token
          }, status=status.HTTP_201_CREATED)


class CustomerRegView(generics.CreateAPIView):
  serializer_class = CustomerSerializer

  def post(self, request):
        """
        create:
          Create a new vendor.
        """  
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token =  AuthToken.objects.create(user)[1]
        return Response({
          "message": "customer created succesfully",
          'customer': serializer.data,
          'token': token
          }, status=status.HTTP_201_CREATED)

class UserLogin(generics.CreateAPIView):
  

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        token =  AuthToken.objects.create(user)[1]
        return Response({
          "message": "Login succesfully",
          'user': serializer.data,
          'token': token
          }, status=status.HTTP_201_CREATED)
