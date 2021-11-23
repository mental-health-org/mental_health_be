from django.test import TestCase
from accounts.models import *
from accounts.serializers import *

class TestUserSerializer(TestCase):

    def setUp(self):
        self.user_attributes = {
                    "username" : 'Orson_Wells',
                    "title" : 'Some Title',
                    "email" : 'test@email.com',
                    "password" : '1a2b3c4d5e',
                    }

        self.user = User.objects.create(**self.user_attributes)
        self.serializer = UserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(["id", "username", "title",
        "email", "is_active", "is_admin", "is_staff", "is_superuser",
        "connections", "last_login", "created_at", "updated_at"]))

    def test_username(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user.username)

    def test_title(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.user.title)

    def test_email(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.user.email)

    def test_connections(self):
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
                                                     user_sent = self.user2,
                                                     user_received = self.user,
                                                     status = 0,
                                                     )
        self.connection2 = Connection.objects.create(
                                                    user_sent = self.user3,
                                                    user_received = self.user,
                                                    status = 1,
                                                    )
        self.connection3 = Connection.objects.create(
                                                    user_sent = self.user,
                                                    user_received = self.user4,
                                                    status = 1,
                                                    )
        data = self.serializer.data
        self.serializer = UserSerializer(instance=self.user)
        self.assertEqual(data['connections']['connected'][0]['name'], self.user3.username)
        self.assertEqual(data['connections']['connected'][1]['name'], self.user4.username)
        self.assertEqual(data['connections']['pending'][0]['name'], self.user2.username)

class TestRegistrationSerializer(TestCase):

    def setUp(self):
        self.user_attributes = {
                    "username" : 'Orson_Wells',
                    "email" : 'email@email.com',
                    "password" : '1a2b3c4d5e',
                    "password2" : '1a2b3c4d5e',
                    }

        self.serializer = RegistrationSerializer(instance=self.user_attributes)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["username", "title", "email"]))
