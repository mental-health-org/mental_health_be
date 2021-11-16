from django.test import TestCase
from accounts.models import *

class TestUserCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = 'Orson_Wells',
                                        email = 'test@email.com',
                                        title = 'counselor',
                                        password = '1a2b3c4d5e',
                                        )

    def test_string_representation_of_user(self):
        expect_representation_user = '{}'.format(self.user.username)
        self.assertEqual(expect_representation_user, str(self.user))

    def test_values_of_user(self):
        self.assertEqual(self.user.username, 'Orson_Wells')
        self.assertEqual(self.user.password, '1a2b3c4d5e')
        self.assertEqual(self.user.title, 'counselor')
        self.assertEqual(self.user.email, 'test@email.com')
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_admin, False)
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.is_staff, False)

    def test_user_token(self):
        self.assertEqual(self.user, Token.objects.first().user)
