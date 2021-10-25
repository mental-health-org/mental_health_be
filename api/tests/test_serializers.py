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

    def test_body_field(self):
        data = self.serializer.data

        self.assertEqual(data['body'], self.response_attributes['body'])

    def test_post_field(self):
        data = self.serializer.data

        self.assertEqual(data['post'], self.post.id)

class TestPostSerializer(TestCase):

    def setUp(self):
        self.post_attributes = { "title": "Test Title", "body": "ipsum lorem" }

        self.post = Post.objects.create(**self.post_attributes)
        self.serializer = PostSerializer(instance=self.post)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(["id", "user", "title", "body",
        "upvote", "downvote", "tagging", "created_at", "updated_at"]))

    def test_title_field(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.post.title)

    def test_body_field(self):
        data = self.serializer.data
        self.assertEqual(data['body'], self.post.body)

    def test_upvote_field(self):
        data = self.serializer.data
        self.assertEqual(data['upvote'], self.post.upvote)

    def test_downvote_field(self):
        data = self.serializer.data
        self.assertEqual(data['downvote'], self.post.downvote)

    def test_tagging_field(self):
        self.tag = Tag.objects.create(name = "Help")
        self.post.tagging.add(self.tag)
        self.serializer = PostSerializer(instance=self.post)

        data = self.serializer.data
        self.assertEqual(data['tagging'][0], self.post.tagging.first().id)
