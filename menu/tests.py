import json

from django.urls import reverse, resolve
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


from .models import Menu
from .serializers import MenuSerializers, UserSerializer
from accounts.models import Vendor, User, Customer
from .views import MenuCreateAPI, MenuDetailsAPI

class MenuUrlsTestCase(APITestCase):
  def test_create_menu_urls(self):
    url = reverse('list')
    self.assertEquals(resolve(url).func.view_class, MenuCreateAPI)

  def test_menu_details_urls(self):
    url = reverse('detail', args=['1'])
    self.assertEquals(resolve(url).func.view_class, MenuDetailsAPI)


class MenuViewsTestCase(APITestCase):
  list_url = reverse('list')

  def setUp(self):
    self.user = Vendor.objects.create_vendor(
      email="davinci@gmail.com", 
      phone_number="08075985865", 
      business_name="Davinci Foods", 
      password="Some_very_strong_password"
      )

    self.token =  AuthToken.objects.create(self.user)[1]
    self.api_aunthenticate()
    self.menu1 = Menu.objects.create(
      name="Test Food", 
      description="Test Description", 
      price= float(2000), 
      quantity= 4,
      isRecurring = True,
      frequencyOfReocurrence = "D",
      vendorId = self.user
    )

  def api_aunthenticate(self):
    self.client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

  def test_menu_list(self):
    response = self.client.get(self.list_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEquals(self.menu1.name, response.data['menu'][0]['name'])

  def test_menu_list_invalid(self):
    self.client.force_authenticate(user=None)
    response = self.client.get(self.list_url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_menu_create(self):
    data = {
      "name": "Food Alayo",
      "description": "Nice test",
      "price": 2000,
      "quantity": 2,
      "isRecurring": True,
      "frequencyOfReocurrence": "D"
      }

    response = self.client.post(self.list_url, data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['menu']['name'], data['name'])
    
  def test_menu_create_unauthorize_user(self):
    data = {
      "name": "Food Alayo 2",
      "description": "Nice test",
      "price": 2000,
      "quantity": 2,
      "isRecurring": True,
      "frequencyOfReocurrence": "D"
      }
    self.client.force_authenticate(user=None)
    response = self.client.post(self.list_url, data)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    count = Menu.objects.count()
    self.assertEqual(count, 1)

  def test_menu_create_unpermitted_user(self):

    user = user = Customer.objects.create_customer(
      email="user2@gmail.com", 
      phone_number="08075985865", 
      first_name="User", 
      last_name="Two", 
      password="Some_very_strong_password"
      )

    token =  AuthToken.objects.create(user)[1]
    self.user = user
    self.client.credentials(HTTP_AUTHORIZATION="Token "+ token)
    data = {
      "name": "Food Alayo 2",
      "description": "Nice test",
      "price": 2000,
      "quantity": 2,
      "isRecurring": True,
      "frequencyOfReocurrence": "D"
      }

    response = self.client.post(self.list_url, data)
    self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    message = 'Only a Vendor can perform this operation'
    self.assertEquals(response.data['detail'], message)
    count = Menu.objects.count()
    self.assertEqual(count, 1)


  # test menu details retrieve by id valid user
  def test_menu_details_retrieve_valid_user(self):
    response = self.client.get(reverse('detail', args=['1']))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(self.menu1.name, response.data['menu']['name'])

  # test menu details retrieve by id invalid user

  def test_menu_details_retrieve_invalid_user(self):
    self.client.force_authenticate(user=None)
    response = self.client.get(reverse('detail', args=['1']))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_retrieve_not_found(self):
    response = self.client.get(reverse('detail', args=['2']))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_menu_detail_update_by_permitted_owner(self):
    Menu.objects.create(
      name="Test Food 2", 
      description="Test Description two", 
      price= float(2000), 
      quantity= 4,
      isRecurring = True,
      frequencyOfReocurrence = "D",
      vendorId = self.user
    )
    
    data = {
      "name": "Amala Delicious",
      "description": "Amala Sumptuos",
      "quantity": 2	
      }

    response = self.client.put(reverse('detail', args=['2']), data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], data['name'])

  def test_menu_detail_update_by_invalid_user(self):
    Menu.objects.create(
      name="Test Food 2", 
      description="Test Description two", 
      price= float(2000), 
      quantity= 4,
      isRecurring = True,
      frequencyOfReocurrence = "D",
      vendorId = self.user
    )
    
    data = {
      "name": "Amala Delicious",
      "description": "Amala Sumptuos",
      "quantity": 2	
      }

    self.client.force_authenticate(user=None)

    response = self.client.put(reverse('detail', args=['2']), data)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


  def test_menu_detail_update_by_unpermitted_user(self):

    user = user = Vendor.objects.create_vendor(
      email="user2@gmail.com", 
      phone_number="08075985865", 
      business_name="User", 
      password="Some_very_strong_password"
      )

    token =  AuthToken.objects.create(user)[1]
    self.user = user
    self.client.credentials(HTTP_AUTHORIZATION="Token "+ token)
    
    data = {
      "name": "Amala Delicious",
      "description": "Amala Sumptuos",
      "quantity": 2	
      }

    response = self.client.put(reverse('detail', args=['1']), data)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_menu_detail_update_by_customer_user(self):

    user = user = Customer.objects.create_customer(
      email="user2@gmail.com", 
      phone_number="08075985865", 
      first_name="User", 
      last_name="Two", 
      password="Some_very_strong_password"
      )

    token =  AuthToken.objects.create(user)[1]
    self.user = user
    self.client.credentials(HTTP_AUTHORIZATION="Token "+ token)
    
    data = {
      "name": "Amala Delicious",
      "description": "Amala Sumptuos",
      "quantity": 2	
      }

    response = self.client.put(reverse('detail', args=['1']), data)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_menu_detail_delete_by_permitted_owner(self):
    Menu.objects.create(
      name="Test Food 2", 
      description="Test Description two", 
      price= float(2000), 
      quantity= 4,
      isRecurring = True,
      frequencyOfReocurrence = "D",
      vendorId = self.user
    )
    
    response = self.client.delete(reverse('detail', args=['2']))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

  def test_menu_detail_delete_by_unpermitted_owner(self):

    user = user = Vendor.objects.create_vendor(
      email="user2@gmail.com", 
      phone_number="08075985865", 
      business_name="User", 
      password="Some_very_strong_password"
      )

    token =  AuthToken.objects.create(user)[1]
    self.user = user
    self.client.credentials(HTTP_AUTHORIZATION="Token "+ token)
    
    response = self.client.delete(reverse('detail', args=['1']))
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_menu_detail_delete_by_invalid(self):
    Menu.objects.create(
      name="Test Food 2", 
      description="Test Description two", 
      price= float(2000), 
      quantity= 4,
      isRecurring = True,
      frequencyOfReocurrence = "D",
      vendorId = self.user
    )
    self.client.force_authenticate(user=None)

    response = self.client.delete(reverse('detail', args=['2']))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_menu_detail_delete_by_customer(self):

    user = user = Customer.objects.create_customer(
      email="user2@gmail.com", 
      phone_number="08075985865", 
      first_name="User", 
      last_name="Two", 
      password="Some_very_strong_password"
      )

    token =  AuthToken.objects.create(user)[1]
    self.user = user
    self.client.credentials(HTTP_AUTHORIZATION="Token "+ token)
    
    response = self.client.delete(reverse('detail', args=['1']))
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)