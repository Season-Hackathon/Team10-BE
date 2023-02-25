from sqlite3 import IntegrityError
from django.shortcuts import get_object_or_404, render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view

from accounts.serializers import AddUserSerializer, CustomUserSerializer
from .models import *
from .serializers import * 
from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from rest_framework.filters import SearchFilter

@api_view(['GET','PATCH','DELETE'])
def mypage_update_delete(request,card_pk):
    card = get_object_or_404(Card,pk=card_pk)
    if request.method == 'GET':
        cards = Card.objects.all()
        def get_queryset(self):
            queryset = Card.objects.filter(tag=None)
        serializer = CardSerializer(cards, many=True)
        return Response(data=serializer.data)
    elif request.method =='PATCH':
        serializer = CardSerializer(instance=card, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    elif request.method=='DELETE':
        card.delete()
        data={
            'card':card_pk
        }
        return Response(data)

@api_view(['POST'])
def create(request):
    if request.method == 'POST':
        serializer = Card2Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)

# 카드 목록 조회
# http://127.0.0.1:8000/card/
class CardAPIView(APIView):
    def get(self, request):
        cards = Card.objects.all()
        serializer = Card2Serializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# 카드 상세 조회
# http://127.0.0.1:8000/card/{user_id}
class CardDetailAPIView(APIView):       
    def get(self, request, user_id):
        user = get_object_or_404(Card, user=user_id)
        serializer = FriendSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FriendAPIView(APIView):
    # 친구 목록 조회
    # http://127.0.0.1:8000/card/{user_id}/friends
     
    def get(self, request, user_id):
       cards = Card.objects.filter(user=user_id)
       serializer = FriendSerializer(cards, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)

# 친구 목록에서 검색
class SearchViewSet(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = FriendSerializer
    region_separator = ","

    def get_queryset(self):
        friends = self.request.query_params.get("friends", None)
        if friends:
            qs = Card.objects.filter()
            for region in friends.split(self.region_separator):
                qs = qs.filter(regions__code=region)
            return qs

        return super().get_queryset()

class FriendCreateView(APIView):
    def post(self, request, user_id):
        
        # user = 나 
        user = get_object_or_404(CustomUser, id=request.data['id'])
        try:
            # 추가할 친구 = 나? => 오류
            if user_id == request.user.id:
                raise IntegrityError
            
            user.friends.add(request.data)
            serializers = AddUserSerializer(data=request.data) 
            if serializers.is_valid():           
                serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)    
        
        except IntegrityError:
            return self.response(message = '잘못된 요청입니다.', status = 400)
        
        
        

# 친구 상세 페이지에서 하트 누르면 (post) 나의 친구 목록에 해당 친구의 id가 추가