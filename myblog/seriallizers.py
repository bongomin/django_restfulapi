from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Post, Tag


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

