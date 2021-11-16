from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .router import router
from questions.views import *

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    #Oauth
    path('accounts/', include('allauth.urls')),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    # API Route Version Control
    path('api/v1/', include(router.urls)),
    # Custom Routes
    path('api/v1/filter/questions/', question_tags_search, name = 'filter_questions'),
    path('api/v1/search/questions/', question_search, name = 'search_questions'),
    # Authorization Routes
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # path('api/v1/login/', auth_views.LoginView.as_view(), name='login')
    # Password Management
    path('accounts/', include('django.contrib.auth.urls')),
]
