from rest_framework.decorators import permission_classes, api_view
from accounts.serializers import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated

from django.contrib.auth import authenticate
import jwt
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from rest_framework import status

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
    user = authenticate(username=username, password=password,name=name,phonenum=phonenum)
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

