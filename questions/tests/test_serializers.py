from django.test import TestCase
from questions.serializers import *

class TestPostSerializer(TestCase):

    def setUp(self):
        self.post_attributes = { "title": "Test Title", "body": "ipsum lorem" }

        self.post = Post.objects.create(**self.post_attributes)
        self.serializer = PostSerializer(instance=self.post)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(["id", "user", "title", "body",
        "quarantine", "votes", "tagging", "created_at", "updated_at"]))

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

class TestSingleQuestionSerializer(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = "Orson Wells", title = "Director")
        self.post_attributes = { "user": self.user, "title": "Test Title", "body": "Test body"}
        self.tag = Tag.objects.create(name = "Test Tag")

        self.post = Post.objects.create(**self.post_attributes)
        self.post.tagging.add(self.tag)
        self.response = Response.objects.create(post = self.post, body = "Test Response")
        self.serializer = SingleQuestionSerializer(instance=self.post)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(['id', 'title', 'body', 'user',
        'tagging', 'responses', 'upvotes', 'downvotes' ,'created_at', 'updated_at']))

    def test_title(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.post.title)

    def test_body(self):
        data = self.serializer.data
        self.assertEqual(data['body'], self.post.body)

    def test_user(self):
        data = self.serializer.data
        self.assertEqual(data["user"]["username"], self.user.username)
        self.assertEqual(data["user"]["title"], self.user.title)

    def test_tagging(self):
        data = self.serializer.data
        self.assertEqual(data["tagging"][0], self.tag.name)

    def test_responses(self):
        data = self.serializer.data
        self.assertEqual(data["responses"][0]["id"], self.response.id)
        self.assertEqual(data["responses"][0]["body"], self.response.body)
        self.assertEqual(data["responses"][0]["upvote"], 0)
        self.assertEqual(data["responses"][0]["downvote"], 0)

    def test_responses_with_user(self):
        self.response = Response.objects.create(user = self.user, post = self.post, body = "Test Response")
        self.serializer = SingleQuestionSerializer(instance=self.post)
        data = self.serializer.data

        self.assertEqual(data["responses"][0]["user"], None)
        self.assertEqual(data["responses"][1]["user"]["username"], self.user.username)
        self.assertEqual(data["responses"][1]["user"]["title"], self.user.title)

    def test_upvotes(self):
        QuestionVotes.objects.create(post = self.post, user = self.user, vote_type = 1)
        self.serializer = SingleQuestionSerializer(instance=self.post)
        data = self.serializer.data

        self.assertEqual(data['upvotes'], 1)

    def test_downvotes(self):
        QuestionVotes.objects.create(post = self.post, user = self.user, vote_type = 2)
        self.serializer = SingleQuestionSerializer(instance=self.post)
        data = self.serializer.data

        self.assertEqual(data['downvotes'], 1)
