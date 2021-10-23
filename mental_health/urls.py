from django.contrib import admin
from django.urls import path, include
from .router import router
from api.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('api/v1/', include(router.urls)),
<<<<<<< HEAD
    path('api/v1/filter/questions/', question_tags_search, name = 'filter_questions'),
    path('api/v1/search/questions/', question_search, name = 'search_questions')
=======
=======
    path('api/v1/', include(router.urls)), #what does this do?
>>>>>>> cbcf88f (Update post responses with get user/post and clean up code; 201 status)
    path('api/v1/', include('api.urls')),
>>>>>>> ec8c2d0 (Setup post responses endpoint; not working)
]
