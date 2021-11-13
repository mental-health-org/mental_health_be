from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length = 30)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    title = models.CharField(max_length = 300)
    body = models.CharField(max_length = 5000, null=True, blank=True, default=None)
    votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_post_vote', through='QuestionVotes')
    tagging = models.ManyToManyField(Tag, related_name='taggings', blank=True)
    quarantine = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

class Response(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, default=None, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=5000)
    votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_response_vote', through='ResponseVote')
    quarantine = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class QuestionVotes(models.Model):
    class Vote(models.IntegerChoices):
        UPVOTE = 1, "upvote"
        DOWNVOTE = 2, "downvote"
        NOVOTE = 3, "novote"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_question_vote', default=None, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_question_vote', default=None, blank=True, on_delete=models.CASCADE)
    vote_type = models.PositiveSmallIntegerField(choices=Vote.choices, default=Vote.NOVOTE)
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
