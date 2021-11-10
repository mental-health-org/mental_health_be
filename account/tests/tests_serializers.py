from django.test import TestCase
from account.models import *
from account.serializers import *

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
        "email", "password", "is_active", "is_admin", "is_staff", "is_superuser",
        "last_login", "created_at", "updated_at"]))

    def test_username(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user.username)

    def test_title(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.user.title)

    def test_email(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.user.email)

    def test_password(self):
        data = self.serializer.data
        self.assertEqual(data['password'], self.user.password)
