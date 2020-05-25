import json

from django.urls import reverse, resolve

from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Customer, User, Vendor
from .serializers import CustomerSerializer, LoginSerializer, VendorSerializer
from .views import VendorRegView, CustomerRegView, UserLogin

# class TestModels(APITestCase):
#   def test_valid_user_model(self):
#     try:
#       User.objects.create_user(email=None, password="Truepossible", phone_number="07098765355")
#     except ValueError:
#       msg = "The given email must be set"
#       self.assertEquals(msg, '')

class TestUrlsCase(APITestCase):
  def test_create_vendor_resolves(self):
    url = reverse('vendor')
    self.assertEquals(resolve(url).func.view_class, VendorRegView)

  def test_create_customer_resolves(self):
    url = reverse('customer')
    self.assertEquals(resolve(url).func.view_class, CustomerRegView)

  def test_login_user_resolves(self):
    url = reverse('login')
    self.assertEquals(resolve(url).func.view_class, UserLogin)

class TestSerializers(APITestCase):
  def test_vendor_serializer_valid(self):
    data = {
      "email": "abbeyunique@gmail.com",
      "phone_number": "07089524255",
      "business_name": "Lade Foods",
      "password": "oluwanisola",
    }
    serializer = VendorSerializer(data=data)
    self.assertTrue(serializer.is_valid())
    
  def test_vendor_serializer_invalid(self):
    data = {}
    serializer = VendorSerializer(data=data)
    self.assertFalse(serializer.is_valid())
    self.assertEquals(len(serializer.errors), 4)

  def test_customer_serializer_valid(self):
    data = {
      "email": "customer@gmail.com",
      "phone_number": "07089524255",
      "first_name": "Best",
      "last_name": "Customer",
      "password": "oluwanisola",
    }
    serializer = CustomerSerializer(data=data)
    self.assertTrue(serializer.is_valid())


  def test_customer_serializer_invalid(self):
    data = {}
    serializer = CustomerSerializer(data=data)
    self.assertFalse(serializer.is_valid())
    self.assertEquals(len(serializer.errors), 3)

  def test_login_serializer_valid(self):
    user_data = {
      "email": "dummy@test.com",
      "phone_number": "0405894578",
      "password": "oluwanisola",
      "business_name": "Lade Foods"
    }
    Vendor.objects.create_vendor(
      email=user_data['email'],
      business_name = user_data['business_name'],
      password=user_data['password'], 
      phone_number=user_data['phone_number']
    )
    data = {
      "email": "dummy@test.com",
      "password": "oluwanisola",
    }
    serializer = LoginSerializer()
    self.assertTrue(serializer.validate(data))

  def test_login_serializer_invalid(self):
    data = {}
    serializer = LoginSerializer(data=data)
    self.assertFalse(serializer.is_valid())
    self.assertEquals(len(serializer.errors), 2)

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

