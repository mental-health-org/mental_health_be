from django.core import serializers as core_serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from responses.models import *

User = get_user_model()

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
