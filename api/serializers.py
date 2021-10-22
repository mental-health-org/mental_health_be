from django.core import serializers as core_serializers
from rest_framework import serializers
from .models import User, Post, Tag


class QuestionsSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'upvote', 'downvote', 'tagging', 'created_at', 'updated_at')

class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'body', 'upvote', 'downvote', 'created_at', 'updated_at')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("__all__")

def basic_serializer(objects):
    return core_serializers.serialize('json', [objects])
