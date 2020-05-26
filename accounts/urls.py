from django.urls import path, include, re_path
from .views import CustomerRegView, VendorRegView, UserLogin, SetPasswordAPI, index
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
from knox import views as knox_views


schema_view = get_schema_view(
    openapi.Info(
        title="Food Vendor API",
        default_version='v1',
        description="A VGC Backend Capstone Project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kayodegabriela@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('', index, name='index'),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger',
                                           cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),
    path('api/auth/signup/vendor', VendorRegView.as_view(), name='vendor'),
    path('api/auth/signup/customer', CustomerRegView.as_view(),  name='customer'),
    path(r'api/auth/login', UserLogin.as_view(),  name='login'),
    path('api/auth/set/password/user/<str:unique_ref>',
         SetPasswordAPI.as_view(),  name='password'),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
]
