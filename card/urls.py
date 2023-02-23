from django.urls import path,include
from .views import *
from . import views
from rest_framework.routers import DefaultRouter

app_name = "card"
urlpatterns = [
    path('create',create,name='create'),
    path('<int:card_pk>/',mypage_update_delete,name='mypage')
]