from django.urls import path,include
from .views import *
from . import views
from rest_framework.routers import DefaultRouter

app_name = "card"
urlpatterns = [
    path('create',create,name='create'),
    path('<int:card_pk>/',mypage_update_delete,name='mypage'),
    path('', CardAPIView.as_view()),
    path('<int:user_id>', CardDetailAPIView.as_view()),
    path('<int:user_id>/friends/', FriendAPIView.as_view()),
    path('<int:user_id>/search', SearchViewSet.as_view()),
    path('<int:user_id>/add', FriendCreateView.as_view())
]