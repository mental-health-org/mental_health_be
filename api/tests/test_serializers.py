from django.test import TestCase
from api.models import *
from api.serializers import *

class TestTagsSerializer(TestCase):

    def setUp(self):
        self.tag_attributes = {"name": "Help"}

        self.tag = Tag.objects.create(**self.tag_attributes)
        self.serializer = TagsSerializer(instance=self.tag)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(["id", "name"]))

    def test_name_field(self):
        data = self.serializer.data

        self.assertEqual(data['name'], self.tag_attributes['name'])

class TestResponseSerializer(TestCase):

    def setUp(self):

        self.post = Post.objects.create(title = 'Test Title', body = 'ipsum lorem')
        self.response_attributes = { "post": self.post, "body": "Some Body"}

        self.response = Response.objects.create(**self.response_attributes)
        self.serializer = ResponseSerializer(instance=self.response)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(["id", "user", "post", "body"]))

