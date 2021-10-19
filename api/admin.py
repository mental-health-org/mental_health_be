from django.contrib import admin
from .models import User, Post, Tag

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Tag)

# Register your models here.
