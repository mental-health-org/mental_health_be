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
        self.user = User.objects.create(username = 'Ipsum')
        self.post = Post.objects.create(title = 'Test Title', body = 'ipsum lorem')
        self.response_attributes = { "post": self.post, "body": "Some Body"}

        self.response = Response.objects.create(**self.response_attributes)
        self.serializer = ResponseSerializer(instance=self.response)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(["id", "user", "upvotes", "downvotes" ,"post", "body"]))

    def test_body_field(self):
        data = self.serializer.data

        self.assertEqual(data['body'], self.response_attributes['body'])

    def test_post_field(self):
        data = self.serializer.data

        self.assertEqual(data['post'], self.post.id)

    def test_upvotes_field(self):
        ResponseVote.objects.create(response = self.response, user = self.user, vote_type = 1)
        self.serializer = ResponseSerializer(instance=self.response)
        data = self.serializer.data

        self.assertEqual(data['upvotes'], 1)

class TestPostSerializer(TestCase):

    def setUp(self):
        self.post_attributes = { "title": "Test Title", "body": "ipsum lorem" }

        self.post = Post.objects.create(**self.post_attributes)
        self.serializer = PostSerializer(instance=self.post)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(["id", "user", "title", "body",
        "votes", "tagging", "created_at", "updated_at"]))

    def test_title_field(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.post.title)

    def test_body_field(self):
        data = self.serializer.data
        self.assertEqual(data['body'], self.post.body)

    def test_tagging_field(self):
        self.tag = Tag.objects.create(name = "Help")
        self.post.tagging.add(self.tag)
        self.serializer = PostSerializer(instance=self.post)

        data = self.serializer.data
        self.assertEqual(data['tagging'][0], self.post.tagging.first().id)

class TestUserSerializer(TestCase):

    def setUp(self):
        self.user_attributes = { "username": "New user" }

        self.user = User.objects.create(**self.user_attributes)
        self.serializer = UserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(["id", "username", "title", "created_at", "updated_at"]))

    def test_username(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user.username)
