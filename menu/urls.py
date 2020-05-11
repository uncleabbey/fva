from django.urls import path, include
from .views import MenuCreateAPI, MenuDetailsAPI

urlpatterns = [
    path('api/v1/menu', MenuCreateAPI.as_view()),
    path('api/v1/menu/<int:id>', MenuDetailsAPI.as_view())
]

