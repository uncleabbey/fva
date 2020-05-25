from django.urls import path, include, re_path
from .views import CustomerRegView, VendorRegView, UserLogin, SetPasswordAPI
from .swagger import SwaggerSchemaView


urlpatterns = [
    path(r'', SwaggerSchemaView.as_view()),
    path('api/auth/signup/vendor', VendorRegView.as_view(), name='vendor'),
    path('api/auth/signup/customer', CustomerRegView.as_view(),  name='customer'),
    path(r'api/auth/login', UserLogin.as_view(),  name='login'),
    path('api/auth/set/password/user/<str:unique_ref>',
         SetPasswordAPI.as_view(),  name='password')
]
