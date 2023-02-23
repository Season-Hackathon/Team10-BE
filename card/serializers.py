from rest_framework import serializers
from .models import *
from accounts.models import CustomUser

    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tagname','tagcontent']

class CardSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    CustomUser = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username')
    class Meta:
        model = Card
        fields = '__all__'
    
    def create_tag(self, validated_data):
        tags_data = validated_data.pop('tags')
        card = Card.objects.create(**validated_data)
        for tag_data in tags_data:
            Tag.objects.create(card=card, **tag_data)
        return card