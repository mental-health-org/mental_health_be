from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
# https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/providers/linkedin_oauth2/views.py
from allauth.socialaccount.providers.linkedin_oauth2 import views as linkedin_views
from accounts.views import *
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .router import router
from questions.views import *

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    #Oauth
    path('accounts/', include('allauth.urls')),
    # path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('auth/', include('rest_auth.urls')),
    path('auth/linkedin/login', linkedin_views.oauth2_login),
    path('auth/linkedin/', LinkedInConnect.as_view()),
    path('auth/linkedin/', linkedin_callback, name='linkedin_callback'),
    # API Route Version Control
    path('api/v1/', include(router.urls)),
    # Custom Routes
    path('api/v1/filter/questions/', question_tags_search, name = 'filter_questions'),
    path('api/v1/search/questions/', question_search, name = 'search_questions'),
    # Authorization Routes
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # path('api/v1/login/', auth_views.LoginView.as_view(), name='login')
    # Password Management
    path('accounts/', include('django.contrib.auth.urls')),
]
