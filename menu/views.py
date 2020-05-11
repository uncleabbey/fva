from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status, views
import cloudinary.uploader
from .serializers import MenuSerializers
from .models import Menu
from accounts.models import Vendor
from rest_framework.generics import get_object_or_404


class MenuCreateAPI(views.APIView):
  parser_classes = (
        MultiPartParser,
        JSONParser,
    )
  queryset =  Menu.objects.all()
  serializer_class = MenuSerializers
  # permission_classes = [
  #       permissions.IsAuthenticated
  #   ]

  def get(self, request):
    menu = Menu.objects.all()
    serializer =  MenuSerializers(menu, many=True)
    return Response(serializer.data)


  @staticmethod
  def post(request):
    # get file from request
    file = request.data.get('img_url')
    upload_data = cloudinary.uploader.upload(file)

    img_url = upload_data['url']

    # get other request data
    name = request.data['name']
    price = float(request.data['price'])
    description = request.data['description']
    quantity = int(request.data['quantity'])
    isRecurring = request.data['isRecurring']
    frequencyOfReocurrence = request.data['frequencyOfReocurrence']
    # get vendor object from its id
    vendorId = int(request.data['vendorId'])
    vendor = Vendor.objects.get(id=vendorId)

    # create menu
    menu = Menu.objects.create(
      img_url= img_url,
      name=name, 
      description=description, 
      price=price, 
      quantity=quantity,
      isRecurring = isRecurring,
      frequencyOfReocurrence = frequencyOfReocurrence,
      vendorId = vendor
      )
  # serialize and send response
    return Response({
      'message': 'Menu added succesfully',
      'menu': MenuSerializers(menu).data
    }, status=status.HTTP_201_CREATED)


class MenuDetailsAPI(views.APIView):
  queryset =  Menu.objects.all()
  serializer_class = MenuSerializers
  # permission_classes = [
  #       permissions.IsAuthenticated
  #   ]


  def get_object(self, id):
      id = int(id)
      try:
          return Menu.objects.get(id=id)
      except Menu.DoesNotExist:
          return HttpResponse(status=status.HTTP_404_NOT_FOUND)

  def get(self, request, id):
    menu = self.get_object(id)
    serializer = MenuSerializers(menu)
    return Response(serializer.data)

  def put(self, request, id):
    menu = self.get_object(id)
    data = request.data
    serializer = MenuSerializers(menu, data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)

  def delete(self, request, id):
    menu = self.get_object(id)
    menu.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)