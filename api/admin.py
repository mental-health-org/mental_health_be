from django.contrib import admin
from .models import User, Post, Tag, Response

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Response)

# Register your models here.
