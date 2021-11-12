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

class TestRegisterViewSets(TestCase):
    def setUp(self):
        # Create Objects
        self.user = {
                    "username" : 'Orson_Wells',
                    "email" : 'test@email.com',
                    "title" : 'profession',
                    "password" : '1a2b3c4d5e',
                    "password2" :'1a2b3c4d5e',
                    }

        # Get URL's
        self.list_url = reverse("register-list")

    def test_registration_create(self):
        response = self.client.post("/api/v1/register/", self.user)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], 'Orson_Wells')
        self.assertEqual(response.data['response'], 'Registration Successful')
        self.assertEqual(response.data['token'], Token.objects.last().key)

    def test_registration_create_400(self):

        response = self.client.post("/api/v1/register/",{"invalid": 2})
        self.assertEqual(response.status_code, 400)

class TestLoginViewSets(TestCase):
    def setUp(self):
        # Create Objects
        self.user = {
                    "username" : 'Orson_Wells',
                    "email" : 'test@email.com',
                    "title" : 'profession',
                    "password" : '1a2b3c4d5e',
                    "password2" :'1a2b3c4d5e',
                    }
        self.login = {
                    "username" : 'test@email.com',
                    "password" : '1a2b3c4d5e'
                    }
        # Get URL's
        self.register_url = reverse("register-list")
        self.login_url = reverse("login-list")

    def test_user_login(self):

        self.client.post(self.register_url, self.user)
        response = self.client.post(self.login_url, self.login)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['response'], 'Successful Login')
        self.assertEqual(response.data['token'], Token.objects.last().key)

class TestLogoutViewSets(TestCase):
    def setUp(self):
        # Create Objects
        self.user = {
                    "username" : 'Orson_Wells',
                    "email" : 'test@email.com',
                    "title" : 'profession',
                    "password" : '1a2b3c4d5e',
                    "password2" :'1a2b3c4d5e',
                    }
        self.login = {
                    "username" : 'test@email.com',
                    "password" : '1a2b3c4d5e'
                    }
        self.logout = {
                    "username" : 'Orson_Wells',
                    }
        # Get URL's
        self.register_url = reverse("register-list")
        self.login_url = reverse("login-list")
        self.logout_url = reverse("logout-list")


    def test_user_logout(self):

        self.client.post(self.register_url, self.user)
        self.client.post(self.login_url, self.login)
        response = self.client.post(self.logout_url, self.logout)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['response'], 'Successfully Logged Out')

class TestConnectionViewSets(TestCase):
    def setUp(self):
        # Create Objects
        self.user = User.objects.create(username = 'Orson_Wells',
                                        email = 'test@email.com',
                                        title = 'counselor',
                                        password = '1a2b3c4d5e',
                                        )
        self.user2 = User.objects.create(username = 'Tommy_Wiseau',
                                        email = 'test2@email.com',
                                        title = 'counselor',
                                        password = '1a2b3c4d5e',
                                        )
        self.user3 = User.objects.create(username = 'Third_User',
                                        email = 'test3@email.com',
                                        title = 'counselor',
                                        password = '1a2b3c4d5e',
                                        )
        self.user4 = User.objects.create(username = 'Fourth_User',
                                        email = 'test4@email.com',
                                        title = 'counselor',
                                        password = '1a2b3c4d5e',
                                        )
        self.connection1 = Connection.objects.create(
                                                    user_sent = self.user3,
                                                    user_received = self.user4,
                                                    status = 0,
                                                    )
        # Payloads
        self.send_request = {
                            "user_sent" : str(self.user.id),
                            "user_received" : str(self.user2.id),
                            "status" : "0"
                            }

        self.accept_request = {
                            "user_sent" : str(self.user.id),
                            "user_received" : str(self.user2.id),
                            "status" : "1"
                            }
        # Get URL's
        self.list_url = reverse("connections-list")
        self.detail_url = reverse("connections-detail", args={self.connection1.id})

    def test_sending_connection_request(self):
        response = self.client.post(self.list_url, self.send_request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Connection.objects.last().user_sent, self.user)
        self.assertEqual(Connection.objects.last().user_received, self.user2)
        self.assertEqual(Connection.objects.last().status, 0)

    def test_accepting_connection_request(self):
        self.client.post(self.list_url, self.send_request)
        response = self.client.post(self.list_url, self.accept_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Connection.objects.last().user_sent, self.user)
        self.assertEqual(Connection.objects.last().user_received, self.user2)
        self.assertEqual(Connection.objects.last().status, 1)

    def test_remove_connection(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Connection.objects.all().count(), 0)
