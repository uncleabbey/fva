from django.urls import path, include, re_path
from .views import CustomerRegView, VendorRegView, UserLogin


urlpatterns = [
    path('api/signup/vendor', VendorRegView.as_view()),
    path('api/signup/customer', CustomerRegView.as_view()),
    path('api/login', UserLogin.as_view())
]


