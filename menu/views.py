from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import (generics, mixins, permissions, status, views,
                            viewsets)
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from accounts.models import User

from .models import Menu
from .permissions import IsOwnerOrReadOnly, IsVendorOrReadOnly
from .serializers import MenuSerializers, UserSerializer, VendorSerializer, MenuCreateSerializers


class MenuCreateAPI(generics.ListCreateAPIView):
    """
      get:
      Return a list of all the existing menus.

      post:
      Create a new menu instance.
    """
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )
    queryset = Menu.objects.all()
    serializer_class = MenuCreateSerializers
    permission_classes = [
        permissions.IsAuthenticated,
        IsVendorOrReadOnly
    ]

    def get(self, request):
        menu = Menu.objects.all()
        serializer = MenuSerializers(menu, many=True)
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
            isRecurring=isRecurring,
            frequencyOfReocurrence=frequencyOfReocurrence,
            vendorId=vendorId
        )
    # serialize and send response
        return Response({
            'message': 'Menu added succesfully',
            'menu': MenuSerializers(menu).data
        }, status=status.HTTP_201_CREATED)


class MenuDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
    """
      get:
      Return a instance of menu with id as parameter.

      put:
      Update the given menu.

      patch:
      Update the given menu.

      delete:
      Delete the given menu.
    """
    queryset = Menu.objects.all()
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        menu = self.get_object(id)
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
