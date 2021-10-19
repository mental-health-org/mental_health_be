from rest_framework import serializers
from .models import User, Post, Tag


class QuestionsSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'upvote', 'downvote', 'tagging', 'created_at')

class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')
