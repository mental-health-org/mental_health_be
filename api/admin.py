from django.contrib import admin
from .models import *
from account.models import *

# From Accounts
admin.site.register(User)

# From API
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Response)
admin.site.register(QuestionVotes)
admin.site.register(ResponseVote)
