from django.urls import path, include
from .views import MenuCreateAPI, MenuDetailsAPI

urlpatterns = [
    path('api/menu', MenuCreateAPI.as_view()),
    path('api/menu/<int:id>', MenuDetailsAPI.as_view())
]

