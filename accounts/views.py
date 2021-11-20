import urllib.parse

from allauth.socialaccount.providers.linkedin_oauth2 import views as linkedin_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.shortcuts import redirect
# from accounts.models import *
from django.urls import reverse
# from allauth.account.adapter import DefaultAccountAdapter
# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from dj_rest_auth.registration.views import SocialLoginView

class LinkedInConnect(SocialLoginView):
    client_class = OAuth2Client
    adapter_class = linkedin_views.LinkedInOAuth2Adapter
    # callback_url = 'linkedin_oauth2_callback'

    @property
    def callback_url(self):
        return self.request.build_absolute_uri(reverse('linkedin_oauth2_callback'))

def linkedin_callback(request):
    params = urllib.parse.urlencode(request.GET)
    print(params)
    # return redirect(f'https://mental-health-fe.herokuapp.com/{params}') #redirect to frontend
    return redirect(f'http://localhost:3000/{params}') #redirect to frontend

# class UserAccountAdapter(DefaultAccountAdapter):
#
#     def new_user(self, request):
#         import pdb; pdb.set_trace()
#         return

    # def save_user(self, request, user, form, commit=True):
    #
    #     import pdb; pdb.set_trace()
    #     user = super(UserAccountAdapter, self).save_user(request)
    #     user.save()

# class UserAccountAdapter(DefaultSocialAccountAdapter):
#
#     def new_user(self, request, sociallogin):
#         import pdb; pdb.set_trace()
#         return
