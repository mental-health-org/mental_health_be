from django.test import TestCase
from api.models import *

class TestUserCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username = 'Orson Wells')

    def test_string_representation_of_user(self):
        expect_representation_user = '{}'.format(self.user.username)
        self.assertEqual(expect_representation_user, str(self.user))

class TestPostCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = 'Orson Wells')
        self.post = Post.objects.create(
            user = self.user,
            title = 'Test Title',
            body = 'ipsum lorem'
        )

    def test_string_representation_of_post(self):
        expect_representation_post = '{}'.format(self.post.title)
        self.assertEqual(expect_representation_post, str(self.post))

class TestTagCase(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(name = 'Help')

    def test_creation_of_tag(self):
        tag_name = 'Help'
        self.assertEqual(tag_name, self.tag.name)

class TestTaggingCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = 'Orson Wells')
        self.tag = Tag.objects.create(name = 'Help')
        self.tag2 = Tag.objects.create(name = 'Not This one')
        self.post = Post.objects.create(
            user = self.user,
            title = 'Test Title',
            body = 'ipsum lorem'
        )
        self.post.tagging.add(self.tag)

    def test_tagging(self):
        self.assertEqual(1, self.post.tagging.all().count())
        self.assertEqual(self.tag, self.post.tagging.first())

class TestResponseCase(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title = 'Test Title', body = 'ipsum lorem')
        self.response1 = Response.objects.create( post = self.post, body = 'something')
        self.response2 = Response.objects.create( post = self.post, body = 'other thing')

    def test_responses(self):
        self.assertEqual(2, self.post.response_set.all().count())
        self.assertEqual(self.response1.body, self.post.response_set.first().body)
