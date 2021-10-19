from api.models import User, Post, Tag
from django.test import TestCase

class TestUserCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username = 'Orson Wells')

    def test_string_representation_of_user(self):
        expect_representation_user = "Orson Wells"
        self.assertEqual(expect_representation_user, str(self.user.username))

class TestPostCase(TestCase):

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

class TestTagCase(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(name = 'Help')

    def test_creation_of_tag(self):
        tag_name = 'Help'
        self.assertEqual(tag_name, self.tag.name)
