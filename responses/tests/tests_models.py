from django.contrib.auth import get_user_model
from django.test import TestCase
from questions.models import *
from responses.models import *

User = get_user_model()

class TestResponseCase(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title = 'Test Title', body = 'ipsum lorem')
        self.response1 = Response.objects.create( post = self.post, body = 'something')
        self.response2 = Response.objects.create( post = self.post, body = 'other thing')

    def test_responses(self):
        self.assertEqual(2, self.post.response_set.all().count())
        self.assertEqual(self.response1.quarantine, False)
        self.assertEqual(self.response1.body, self.post.response_set.first().body)

class TestResponseVoteCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = 'Orson_Wells',
                                        email = 'test@email.com',
                                        password = '1a2b3c4d5e',
                                        )
        self.post = Post.objects.create( user = self.user, title = 'Test Title')
        self.response = Response.objects.create(user = self.user, post = self.post, body = 'ipsum lorem')

        ResponseVote.objects.create(user = self.user, response =  self.response, vote_type = 1)
        ResponseVote.objects.create(user = self.user, response =  self.response, vote_type = 2)

    def test_questions_vote(self):
        self.assertEqual(2, self.response.votes.count())

class TestResponseFlagCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = 'Orson_Wells',
                                        email = 'test@email.com',
                                        title = 'professional',
                                        password = '1a2b3c4d5e',
                                        )
        self.post = Post.objects.create( user = self.user, title = 'Test Title', body = 'ipsum lorem')
        self.response = Response.objects.create(user = self.user, post = self.post, body = 'ipsum lorem')

        self.responseflag = ResponseFlag.objects.create(user = self.user, response = self.response, comment = "This is not a relevent response")

    def test_response_flag(self):
        self.assertEqual(1, ResponseFlag.objects.count())
        self.assertEqual(self.responseflag.user, self.user)
        self.assertEqual(self.responseflag.response, self.response)
        self.assertEqual(self.responseflag.status, 0)
        self.assertEqual(self.responseflag.comment, "This is not a relevent response")
