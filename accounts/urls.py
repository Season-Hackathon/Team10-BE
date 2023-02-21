from django.urls import path
from .views import *

urlpatterns = [
    path("regist", user_regist, name="regist"),
    path("login",user_login, name="login"),
    path("test",test,name="test")
]
