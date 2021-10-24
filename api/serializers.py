from django.core import serializers as core_serializers
from rest_framework import serializers
from .models import *


class QuestionsSerializer(serializers.ModelSerializer):
    tagging = serializers.SerializerMethodField()
    response_count = serializers.SerializerMethodField()

    def get_tagging(self, obj):
        tag_names = []
        for tag in obj.tagging.all():
            tag_names.append(tag.name)
        return tag_names

    def get_response_count(self, obj):
<<<<<<< HEAD
        return obj.response_set.all().count()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'response_count','upvote', 'downvote', 'tagging', 'created_at', 'updated_at')
=======
        return obj.response_set.count()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'upvote', 'downvote', 'tagging', 'response_count', 'created_at', 'updated_at')
>>>>>>> 6757a12 (Add response_count to questions endpoint)

class SingleQuestionSerializer(serializers.ModelSerializer):
    tagging = serializers.SerializerMethodField()
    responses = serializers.SerializerMethodField()

    def get_tagging(self, obj):
        tag_names = []
        for tag in obj.tagging.all():
            tag_names.append(tag.name)
        return tag_names

    def get_responses(self, obj):
        responses = []
        for response in obj.response_set.all():
            responses.append(response.body)
        return responses

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'upvote', 'downvote', 'tagging', 'responses' ,'created_at', 'updated_at')

class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')

class ResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Response
        fields = ('id', 'user', 'post', 'body')

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("__all__")

def tags_serializer(queryset):
    all_tags = []
    for tag in queryset:
        all_tags.append(tag.name)
    return {"id": None, "type": "tags", "attributes" : all_tags}

def basic_serializer(objects):
    return core_serializers.serialize('json', [objects])

def header_serializer(type, attributes):
    return { 'id': None, 'type': type, 'attributes': attributes }
