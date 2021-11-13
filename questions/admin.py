from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(QuestionVotes)
admin.site.register(QuestionFlag)
