import urllib.parse
from django.conf import settings

from allauth.socialaccount.providers.linkedin_oauth2 import views as linkedin_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.shortcuts import redirect
from django.urls import reverse
from dj_rest_auth.registration.views import SocialLoginView
from .models import *
from django.dispatch import receiver
import random
from allauth.account.signals import user_signed_up

class LinkedInConnect(SocialLoginView):
    client_class = OAuth2Client
    adapter_class = linkedin_views.LinkedInOAuth2Adapter

    @property
    def callback_url(self):
        return self.request.build_absolute_uri(reverse('linkedin_oauth2_callback'))

def linkedin_callback(request):
    params = urllib.parse.urlencode(request.GET)
    print(params)
    return redirect(f'https://mental-health-fe.herokuapp.com/{params}') #redirect to frontend

@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):
    if sociallogin.account.provider == 'linkedin_oauth2':
        data = user.socialaccount_set.last().extra_data
        name = data['firstName']['localized']['en_US']+data['lastName']['localized']['en_US'][0]
        user.username = name+'_'+''.join(random.sample('0123456789', 9))
        user.title = 'LinkedIn User'

    user.save()
