from django.urls import path, include, re_path
from .views import CustomerRegView, VendorRegView, UserLogin


urlpatterns = [
    path('api/signup/vendor', VendorRegView.as_view(), name='vendor'),
    path('api/signup/customer', CustomerRegView.as_view(),  name='customer'),
    path('api/login', UserLogin.as_view(),  name='login')
]


