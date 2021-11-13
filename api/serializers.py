from django.core import serializers as core_serializers
from rest_framework import serializers
from .models import *
from account.models import *


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

    def get_responses(self, obj):

        responses = []
        for response in obj.response_set.all():
            response_data = {}
            response_data['id'] = response.id
            response_data['body'] = response.body
            response_data['user'] = response.user
            response_data['upvote']= ResponseVote.objects.filter(vote_type = 1, response=response.id).count()
            response_data['downvote'] = ResponseVote.objects.filter(vote_type = 2, response=response.id).count()
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
        fields = ('id', 'title', 'body', 'user', 'tagging', 'responses', 'upvotes', 'downvotes' ,'created_at', 'updated_at')

class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')

class ResponseSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()

    def get_upvotes(self, obj):
        return ResponseVote.objects.filter(vote_type = 1, response=obj.id).count()

    def get_downvotes(self, obj):
        return ResponseVote.objects.filter(vote_type = 2, response=obj.id).count()

    class Meta:
        model = Response
        fields = ('id', 'user', 'post','upvotes', 'downvotes', 'body')

class PostSerializer(serializers.ModelSerializer):


    class Meta:
        model = Post
        fields = ('__all__')

def tags_serializer(queryset):
    all_tags = []
    for tag in queryset:
        all_tags.append(tag.name)
    return {"id": None, "type": "tags", "attributes" : all_tags}

def header_serializer(type, attributes):
    return { 'id': None, 'type': type, 'attributes': attributes }

class QuestionFlagSerializer(serializers.ModelSerializer):


    class Meta:
        model = QuestionFlag
        fields = ('__all__')

class ListQuestionFlagSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionFlag
        fields = ('__all__')

class DetailedQuestionFlagSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = list()
        all_flags = QuestionFlag.objects.filter(post = obj.post.id)
        for flag in all_flags:
            user = User.objects.filter(id = flag.user.id).first()
            details = {"id" : flag.id, "user_id" : user.id, "username" : user.username ,"comment" : flag.comment}
            comments.append(details)
        return comments

    class Meta:
        model = QuestionFlag
        fields = ('id', 'post', 'user', 'status','comments', 'created_at', 'updated_at')

class ResponseFlagSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResponseFlag
        fields = ('__all__')

class DetailedResponseFlagSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = list()
        all_flags = ResponseFlag.objects.filter(response = obj.response.id)
        for flag in all_flags:
            user = User.objects.filter(id = flag.user.id).first()
            details = {"id" : flag.id, "user_id" : user.id, "username" : user.username ,"comment" : flag.comment}
            comments.append(details)
        return comments

    class Meta:
        model = ResponseFlag
        fields = ('id', 'response', 'user', 'status','comments', 'created_at', 'updated_at')

class ListResponseFlagSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResponseFlag
        fields = ('__all__')
