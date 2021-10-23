from django.contrib import admin
from django.urls import path, include
from .router import router
from api.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/filter/questions/', question_tags_search, name = 'filter_questions'),
    path('api/v1/search/questions/', question_search, name = 'search_questions')
]
