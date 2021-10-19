from rest_framework import serializers
from .models import User, Post, Tag


class QuestionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'upvote', 'downvote', 'tagging', 'created_at')
