from api.models import User
from api.models import Post
from django.test import TestCase

class UserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username = 'Orson Wells')

    def test_string_representation_of_user(self):
        expect_representation_user = "Orson Wells"
        self.assertEqual(expect_representation_user, str(self.user.username))

class PostTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = 'Orson Wells')
        self.post = Post.objects.create(
            user = self.user,
            title = 'Test Title',
            body = 'ipsum lorem'
        )

    def test_string_representation_of_post(self):
        expect_representation_post = 'belongs to: {} title: {} body: {}'.format(
            self.post.user.username,
            self.post.title,
            self.post.body
        )
        self.assertEqual(expect_representation_post, str(self.post))
        self.assertEqual(0, self.post.upvote)
        self.assertEqual(0, self.post.downvote)
