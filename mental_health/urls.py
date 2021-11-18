from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
# https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/providers/linkedin_oauth2/views.py
from allauth.socialaccount.providers.linkedin_oauth2 import views as linkedin_views
from accounts import views as account_views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .router import router
from questions.views import *

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    #Oauth
    # path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration', include('dj_rest_auth.registration')),
    path('auth/linkedin/', account_views.LinkedInConnect.as_view()),
    path('auth/linkedin/login/', linkedin_views.oauth2_login, name='linkedin_login'),
    path('auth/linkedin/callback/', account_views.linkedin_callback, name='linkedin_oauth2_callback'),
    # API Route Version Control
    path('api/v1/', include(router.urls)),
    # Custom Routes
    path('api/v1/filter/questions/', question_tags_search, name = 'filter_questions'),
    path('api/v1/search/questions/', question_search, name = 'search_questions'),
    # Password Management
    path('accounts/', include('django.contrib.auth.urls')),
]
