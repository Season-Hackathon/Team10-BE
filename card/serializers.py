from rest_framework import serializers
from .models import *
from accounts.models import CustomUser

    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    CustomUser = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username')
    class Meta:
        model = Card
        fields = '__all__'
    
    def get_tag(self, instance):
        # recursive
        response = super().get_tag(instance)
        response['tag'] = TagSerializer(instance.child).data
        return response

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']

class Card2Serializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source = 'user.username')
    friends = UsernameSerializer(many=True)
    class Meta:
        model = Card
        fields = ['id', 'username', 'classname', 'friends']
        # fields = '__all__'
        # fields = ['friends']


class FriendSerializer(serializers.ModelSerializer):
    # username = serializers.ReadOnlyField(source = 'user.username')
    # friends = UsernameSerializer(many=True)
    # friends_ = serializers.ReadOnlyField(source = 'friends')
    class Meta:
        model = Card
        fields = ['friends']
        
class Friend2Serializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model = Card
        fields = ['username']


