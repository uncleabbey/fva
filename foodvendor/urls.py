from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer


schema_view = get_schema_view(title='FVA API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('', include('accounts.urls')),
    path('', include('menu.urls')),
    path(r'docs/', include_docs_urls(title='FVA API')),
    path(r'swagger-docs/', schema_view),
    path('admin/', admin.site.urls),
]

