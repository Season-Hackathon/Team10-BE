from django.urls import path
from .views import *

urlpatterns = [
    path('', UserList.as_view()),
    path('current/',current_user),
    path("auth/profile/<int:user_pk>/update/",ProfileUpdateAPI.as_view()),
    path('validate/',validate_jwt_token),
]
