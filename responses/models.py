from django.conf import settings
from questions.models import *
from django.db import models

class Response(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, default=None, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=5000)
    votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_response_vote', through='ResponseVote')
    quarantine = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ResponseVote(models.Model):
    class Vote(models.IntegerChoices):
        UPVOTE = 1, "upvote"
        DOWNVOTE = 2, "downvote"
        NOVOTE = 3, "novote"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_comment_vote', default=None, blank=True, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, related_name='response_comment_vote', default=None, blank=True, on_delete=models.CASCADE)
    vote_type = models.PositiveSmallIntegerField(choices=Vote.choices, default=Vote.NOVOTE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ResponseFlag(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 0, "pending"
        SAFE = 1, "safe"
        QUARANTINED = 2, "quarantined"

    response = models.ForeignKey(Response, related_name='response_flag', default=None, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_flagging_response', default=None, blank=True, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
