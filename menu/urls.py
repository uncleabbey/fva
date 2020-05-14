from django.urls import path, include
from .views import MenuCreateAPI, MenuDetailsAPI

urlpatterns = [
    path('menu', MenuCreateAPI.as_view(), name='list'),
    path('menu/<int:id>', MenuDetailsAPI.as_view(), name='detail')
]

# r'^bucketlists/(?P<pk>[0-9]+)/$'