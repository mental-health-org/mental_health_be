from django.contrib.auth import get_user_model
from responses.serializers import *
from django.test import TestCase
from responses.models import *
from questions.models import *

User = get_user_model()

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

    def test_downvotes_field(self):
        ResponseVote.objects.create(response = self.response, user = self.user, vote_type = 2)
        self.serializer = ResponseSerializer(instance=self.response)
        data = self.serializer.data

        self.assertEqual(data['downvotes'], 1)
