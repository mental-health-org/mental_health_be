from django.core import serializers as core_serializers
from rest_framework import serializers
from .models import *


class QuestionsSerializer(serializers.ModelSerializer):
    tagging = serializers.SerializerMethodField()
    response_count = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()

    def get_upvotes(self, obj):
        return QuestionVotes.objects.filter(vote_type = 1, post=obj.id).count()

    def get_downvotes(self, obj):
        return QuestionVotes.objects.filter(vote_type = 2, post=obj.id).count()

    def get_tagging(self, obj):
        tag_names = []
        for tag in obj.tagging.all():
            tag_names.append(tag.name)
        return tag_names

    def get_response_count(self, obj):
        return obj.response_set.count()

    def get_user(self, obj):
        user_data = obj.user
        if obj.user!=None:
            user_data = {}
            user_data["username"] = obj.user.username
            user_data["title"] = obj.user.title
        return user_data

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'user', 'response_count', 'tagging', 'upvotes', 'downvotes', 'created_at', 'updated_at')

class SingleQuestionSerializer(serializers.ModelSerializer):
    tagging = serializers.SerializerMethodField()
    responses = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_tagging(self, obj):
        tag_names = []
        for tag in obj.tagging.all():
            tag_names.append(tag.name)
        return tag_names

    def get_responses(self, obj):
        responses = []
        for response in obj.response_set.all():
            response_data = {}
            response_data['body'] = response.body
            response_data['user'] = response.user
            response_data['created_at'] = response.created_at
            if response.user!=None:
                response_data['user'] = {}
                response_data['user']['username'] = response.user.username
                response_data['user']['title'] = response.user.title
            responses.append(response_data)
        return responses

    def get_user(self, obj):
        user_data = obj.user
        if obj.user!=None:
            user_data = {}
            user_data["username"] = obj.user.username
            user_data["title"] = obj.user.title
        return user_data

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'user', 'upvote', 'downvote', 'tagging', 'responses' ,'created_at', 'updated_at')

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
