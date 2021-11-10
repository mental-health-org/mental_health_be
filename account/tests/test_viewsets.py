from django.test import TestCase
from api.models import *
from account.models import *
from django.urls import reverse
from django.test.client import RequestFactory
import json

class TestUsersViewSets(TestCase):
    def setUp(self):
        # Create Objects
        self.user = User.objects.create(username = 'Orson_Wells',
                                        email = 'test@email.com',
                                        title = 'counselor',
                                        password = '1a2b3c4d5e',
                                        )

        # Get URL's
        self.detail_url = reverse("users-detail", args={self.user.id})
        self.detail_url_404 = reverse('users-detail', args={0})

    def test_users_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.user.username)

    def test_users_detail_404(self):
        response = self.client.get(self.detail_url_404)
        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        response = self.client.delete("/api/v1/users/"+str(self.user.id)+"/", content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.all().count(), 0)

    def test_users_patch(self):
        old_username = User.objects.last().username
        response = self.client.patch("/api/v1/users/"+str(self.user.id)+"/", data={"username": "gooduser"}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(User.objects.last().username, old_username)

