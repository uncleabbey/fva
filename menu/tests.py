import json

from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Menu
from .serializers import MenuSerializers, UserSerializer
from accounts.models import Vendor, User




class CreateMenuTestCase(APITestCase):
  # list_url = reverse('menu-list')

  def setUp(self):
    self.user = Vendor.objects.create_vendor(
      email="davinci@gmail.com", 
      phone_number="08075985865", 
      business_name="Davinci Foods", 
      password="Some_very_strong_password"
      )

    self.token =  AuthToken.objects.create(self.user)[1]
    self.api_aunthenticate()

  def api_aunthenticate(self):
    self.client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)


  def test_menu_create(self):
    data = {
      "name": "Food Alayo",
      "description": "Nice test",
      "price": 2000,
      "quantity": 2,
      "isRecurring": True,
      "frequencyOfReocurrence": "D"
      }

    response = self.client.post('/api/menu', data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['menu']['name'], data['name'])

  def test_menu_list(self):
    response = self.client.get('/api/menu')
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_menu_list_invalid(self):
    self.client.force_authenticate(user=None)
    response = self.client.get('/api/menu')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  # def test_menu_details_retrieve(self):
  #   response = self.client.get('/api/menu/1')
  #   self.assertEqual(response.status_code, status.HTTP_200_OK)


