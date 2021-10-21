from django.conf import settings
from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length = 30, unique=True, error_messages={
        'unique': 'Name is already taken'
    })
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.username

class Tag(models.Model):
    name = models.CharField(max_length = 30)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    title = models.CharField(max_length = 50)
    body = models.CharField(max_length = 1000)
    upvote = models.IntegerField(default = 0)
    downvote = models.IntegerField(default = 0)
    tagging = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title
