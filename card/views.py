from django.shortcuts import get_object_or_404, render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import * 
from django.shortcuts import render,get_object_or_404

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
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)
