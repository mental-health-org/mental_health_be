from django.contrib.auth import get_user_model
from django.test import TestCase
from questions.models import *
from tags.models import *

User = get_user_model()

class TestTagCase(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(name = 'Help')

    def test_creation_of_tag(self):
        tag_name = 'Help'
        self.assertEqual(tag_name, self.tag.name)

    def test_string_representation_of_tag(self):
        expect_representation_tag = '{}'.format(self.tag.name)
        self.assertEqual(expect_representation_tag, str(self.tag))

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
        self.assertEqual(1, self.post.tagging.count())
        self.assertEqual(self.tag, self.post.tagging.first())
