from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes, api_view
from accounts.serializers import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView

from django.contrib.auth import authenticate
import jwt
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from rest_framework import status, generics
from .models import *
from rest_framework.filters import SearchFilter

@api_view(["POST"])
@permission_classes([AllowAny])
def user_regist(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    print(request.data)
    username = request.data.get("username")
    password = request.data.get("password")
    first_naem=request.data.get("first_name")
    email=request.data.get("email")
    user = authenticate(username=username, password=password, first_naem=first_naem)
    if user is not None and user.is_active:
        expired_at = (timezone.now()+timedelta(days=14)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        access_token = jwt.encode(
            {"user_id":user.id},settings.SECRET_KEY)
        return Response(access_token)
    return Response("Invalid id or password", status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test(request):
    return Response(request.user.id)

class UserAPIView(APIView): 
    # http://127.0.0.1:8000/accounts/users/
    # 가입한 전체 유저 조회 
    def get(self, request):
        users = CustomUser.objects.all() # 일단 모든 정보 다 불러옴
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailAPIView(APIView):
    # http://127.0.0.1:8000/accounts/users/{pk}/
    # 가입한 유저 세부 조회 
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserViewSet(generics.ListAPIView):
    # http://127.0.0.1:8000/accounts/search?username={keyword}
    # 가입한 전체 유저 중에 keyword를 포함한 username을 가진 유저 조회
    serializer_class = CustomUserSerializer
    def get_queryset(self):
        queryset = CustomUser.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username__contains=username)
        return queryset