from django.urls import path
from .views import MenuCreateAPI, MenuDetailsAPI

urlpatterns = [
    path('api/menu', MenuCreateAPI.as_view(), name='list'),
    path('api/menu/<int:id>', MenuDetailsAPI.as_view(), name='detail')
]
