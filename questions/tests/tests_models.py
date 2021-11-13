from django.contrib.auth import get_user_model
from django.test import TestCase
from questions.models import *

User = get_user_model()

class TestPostCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = 'Orson_Wells',
                                        email = 'test@email.com',
                                        password = '1a2b3c4d5e',
                                        )
        self.post = Post.objects.create(
            user = self.user,
            title = 'Test Title',
            body = 'ipsum lorem'
        )

    def test_string_representation_of_post(self):
        expect_representation_post = '{}'.format(self.post.title)
        self.assertEqual(expect_representation_post, str(self.post))

    def test_responses(self):
        self.assertEqual(1, Post.objects.count())
        self.assertEqual(self.post.quarantine, False)
        self.assertEqual(self.post.body, Post.objects.first().body)

class TestQuestionVoteCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = 'Orson Wells')
        self.post = Post.objects.create( user = self.user, title = 'Test Title', body = 'ipsum lorem')

        QuestionVotes.objects.create(user = self.user, post =  self.post, vote_type = 1)
        QuestionVotes.objects.create(user = self.user, post =  self.post, vote_type = 2)

    def test_questions_vote(self):
        self.assertEqual(2, self.post.votes.count())


class TestQuestionsFlagCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = 'Orson_Wells',
                                        email = 'test@email.com',
                                        title = 'professional',
                                        password = '1a2b3c4d5e',
                                        )
        self.post = Post.objects.create( user = self.user, title = 'Test Title', body = 'ipsum lorem')

        self.questionflag = QuestionFlag.objects.create(user = self.user, post = self.post, comment = "This is not a relevent question")

    def test_questions_flag(self):
        self.assertEqual(1, QuestionFlag.objects.count())
        self.assertEqual(self.questionflag.user, self.user)
        self.assertEqual(self.questionflag.post, self.post)
        self.assertEqual(self.questionflag.status, 0)
        self.assertEqual(self.questionflag.comment, "This is not a relevent question")
