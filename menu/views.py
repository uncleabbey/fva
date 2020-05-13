from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status, views, generics
import cloudinary.uploader
from .serializers import MenuSerializers, VendorSerializer, UserSerializer
from .models import Menu
from accounts.models import User
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly, IsVendorOrReadOnly

class MenuCreateAPI(generics.ListCreateAPIView):
  parser_classes = (
        MultiPartParser,
        JSONParser,
    )
  queryset =  Menu.objects.all()
  serializer_class = MenuSerializers
  permission_classes = [
        permissions.IsAuthenticated,
        IsVendorOrReadOnly
    ]

  def get(self, request):
    menu = Menu.objects.all()
    serializer =  MenuSerializers(menu, many=True)
    return Response({
      'message': 'success',
      'menu': serializer.data
      })

  def post(self, request):
    name = request.data['name']
    price = float(request.data['price'])
    description = request.data['description']
    quantity = int(request.data['quantity'])
    isRecurring = request.data['isRecurring']
    frequencyOfReocurrence = request.data['frequencyOfReocurrence']
    # get vendor object from its id
    vendorId = request.user

    # create menu
    menu = Menu.objects.create(
      name=name, 
      description=description, 
      price=price, 
      quantity=quantity,
      isRecurring = isRecurring,
      frequencyOfReocurrence = frequencyOfReocurrence,
      vendorId = vendorId
      )
  # serialize and send response
    return Response({
      'message': 'Menu added succesfully',
      'menu': MenuSerializers(menu).data
    }, status=status.HTTP_201_CREATED)


class MenuDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
  queryset =  Menu.objects.all()
  serializer_class = MenuSerializers
  permission_classes = [
        permissions.IsAuthenticated,
        IsVendorOrReadOnly,
        IsOwnerOrReadOnly
    ]


  def get_object(self, id):
      id = int(id)
      obj = get_object_or_404(Menu, id=id)
      self.check_object_permissions(self.request, obj)
      return obj

  def get(self, request, id):
    menu = self.get_object(id)
    serializer = MenuSerializers(menu)
    return Response({
      'menu': serializer.data
      })

  def put(self, request, id):
    menu = self.get_object(id)
    data = request.data
    serializer = MenuSerializers(menu, data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)

  def delete(self, request, id):
    menu = self.get_object(id)
    menu.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)