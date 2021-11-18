import urllib.parse

from allauth.socialaccount.providers.linkedin_oauth2 import views as linkedin_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.shortcuts import redirect
from django.urls import reverse
from rest_auth.registration.views import SocialLoginView

class LinkedInConnect(SocialLoginView):
    client_class = OAuth2Client
    adapter_class = linkedin_views.LinkedInOAuth2Adapter

    @property
    def callback_url(self):
        return self.request.build_absolute_uri(reverse('linkedin_callback'))

def linkedin_callback(request):
    params = urllib.parse.urlencode(request.GET)
    print(params)
    return redirect(f'https://mental-health-fe.herokuapp.com/{params}') #redirect to frontend
