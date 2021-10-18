from api.models import User
from django.test import TestCase

class UserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username = 'Orson Wells')

    def test_string_representation_of_user(self):
        expect_representation_user = "Orson Wells"
        self.assertEqual(expect_representation_user, str(self.user.username))
