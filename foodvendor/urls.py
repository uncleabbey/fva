from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('', include('accounts.urls')),
    path('', include('menu.urls')),
    path('', include('order.urls')),
    path(r'docs/', include_docs_urls(title='FVA API')),
    path('admin/', admin.site.urls),
]
