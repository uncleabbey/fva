import json

from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Customer, User, Vendor
from .serializers import CustomerSerializer, LoginSerializer, VendorSerializer


class VendorRegTestCase(APITestCase):
  def test_registration(self):
    data = {
      "email": "testcase@test.com",
      "password": "some_strong_password",
      "business_name": "Test Case",
      "phone_number": "1234567899",
    }
    response = self.client.post('/api/signup/vendor', data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):
  def setUp(self):
    user_data = {
      "email": "dummy@test.com",
      "phone_number": "0405894578",
      "password": "oluwanisola"
    }
    self.new_user = User.objects.create_user(email=user_data['email'], password=user_data['password'], phone_number=user_data['phone_number'])

  def test_user_login(self):
    data = {
      "email": "dummy@test.com",
      "password": "oluwanisola"
    }
    
    # response = self.client.post('/api/login', data)
    response = self.client.login(email=data['email'], password=data['password'])
    self.assertEqual(response, True)

  def test_inavalid_user(self):
    data = {
      "email": "dummy@test.com",
      "password": "kayode"
    }
    
    response = self.client.login(email=data['email'], password=data['password'])
    self.assertEqual(response, False)

class CustomerRegTestCase(APITestCase):
  def test_registration(self):
    data = {
      "email": "testcase2@test.com",
      "password": "some_strong_password",
      "first_name": "Test Chairman",
      "last_name": "Case Baba",
      "phone_number": "1234567899",
    }
    response = self.client.post('/api/signup/customer', data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

