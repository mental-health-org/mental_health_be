from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Response)
admin.site.register(QuestionVotes)
admin.site.register(ResponseVote)
