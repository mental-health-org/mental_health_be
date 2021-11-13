from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from django.test import TestCase
from questions.models import *
from django.urls import reverse

User = get_user_model()

class TestQuestionsViewSets(TestCase):

    def setUp(self):
        # Create Objects
        self.user = User.objects.create(username = 'Orson Wells')
        self.post = Post.objects.create( user = self.user, title = 'Test Title',
            body = 'ipsum lorem'
        )
        self.post2 = Post.objects.create( user = self.user, title = 'Second Title',
            body = 'dolor sit amet'
        )

        # Get URL's
        self.list_url = reverse('questions-list')
        self.detail_url = reverse('questions-detail', args={self.post2.id})
        self.detail_url_404 = reverse('questions-detail', args={0})

    def test_questions_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_questions_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.post2.id)
        self.assertEqual(response.data['title'], self.post2.title)

    def test_questions_detail_404(self):
        response = self.client.get(self.detail_url_404)
        self.assertEqual(response.status_code, 404)

    def test_questions_create(self):
        self.tag = Tag.objects.create(name='Anxiety')
        self.assertEqual(1, len(Tag.objects.all()))

        response = self.client.post("/api/v1/questions/",{"title": "Third Title",
            "body": "some thoughtful question",
            "tags": ["Depression", "Anxiety"]})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(2, len(Tag.objects.all()))

    def test_questions_create_400(self):

        response = self.client.post("/api/v1/questions/",{"invalid": "nothing",
            "bad input": 2,
            "tags": ["Depression", "Anxiety"]})
        self.assertEqual(response.status_code, 400)

    def test_questions_delete(self):
        response = self.client.delete("/api/v1/questions/"+str(self.post2.id)+"/", content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.all().count(), 1)

    def test_questions_patch(self):
        old_title = Post.objects.last().title
        response = self.client.patch("/api/v1/questions/"+str(self.post2.id)+"/", data={"title": "something new"}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(Post.objects.last().title, old_title)

class TestQuestionVoteViewSet(TestCase):

    def setUp(self):
        # Create Objects
        self.user = User.objects.create(username = 'Orson Wells')
        self.post = Post.objects.create( user = self.user, title = 'Test Title', body = 'ipsum lorem')

    def test_question_votes_create(self):
        response = self.client.post("/api/v1/qvote/", {"user": str(self.user.id), "post": str(self.post.id), "vote_type": "1"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(1, len(QuestionVotes.objects.all()))
        self.assertEqual(1, QuestionVotes.objects.first().vote_type)

        # Vote type can be changed to downvote
        response = self.client.post("/api/v1/qvote/", {"user": str(self.user.id), "post": str(self.post.id), "vote_type": "2"})
        self.assertEqual(1, len(QuestionVotes.objects.all()))
        self.assertEqual(2, QuestionVotes.objects.first().vote_type)

        # Vote type can be changed to novote
        response = self.client.post("/api/v1/qvote/", {"user": str(self.user.id), "post": str(self.post.id), "vote_type": "2"})
        self.assertEqual(1, len(QuestionVotes.objects.all()))
        self.assertEqual(3, QuestionVotes.objects.first().vote_type)

class TestQuestionFlagVoteViewSet(TestCase):

    def setUp(self):
        # Create Objects
        self.user = User.objects.create(username = 'Orson Wells')
        self.admin_user = User.objects.create(username = 'Admin', password = 'password', email = 'admin@admin.email', is_admin = True)
        self.post = Post.objects.create( user = self.user, title = 'Test Title', body = 'ipsum lorem')
        self.qflag = QuestionFlag.objects.create(user = self.user, post = self.post, comment = "bad post")

        self.user2 = User.objects.create(username = 'Second_User', email = '1@email.com')
        self.user3 = User.objects.create(username = 'Third_User', email = '2@email.com')
        self.user4 = User.objects.create(username = 'Fourth_User', email = '3@email.com')

        self.qflag2 = QuestionFlag.objects.create(user = self.user2, post = self.post, comment = "second comment")
        self.qflag3 = QuestionFlag.objects.create(user = self.user3, post = self.post, comment = "third comment")
        self.qflag4 = QuestionFlag.objects.create(user = self.user4, post = self.post, comment = "fourth comment")


        # Get URL's
        self.list_url = reverse('qflag-list')
        self.detail_url = reverse('qflag-detail', args = {str(self.qflag.id)})

        self.request_factory = RequestFactory()

    def test_question_flags_create(self):
        response = self.client.post(self.list_url, {"user": str(self.user.id), "post": str(self.post.id), "comment": "bad post"})
        self.assertEqual(5, QuestionFlag.objects.count())
        self.assertEqual(201, response.status_code)

    def test_question_flags_create_no_starting_items(self):
        QuestionFlag.objects.all().delete()
        response = self.client.post(self.list_url, {"user": str(self.user.id), "post": str(self.post.id), "comment": "bad post"})
        self.assertEqual(1, QuestionFlag.objects.count())
        self.assertEqual(201, response.status_code)

    def test_question_flags_list(self):
        self.post2 = Post.objects.create( user = self.user, title = 'Test Title', body = 'ipsum lorem')
        qflag5 = QuestionFlag.objects.create(user = self.user, post = self.post2, comment = "this is a second post")

        response = self.client.get(self.list_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data[0]['post'], self.post.id)
        self.assertEqual(response.data[0]['status'], 0)
        self.assertEqual(response.data[1]['post'], self.post2.id)
        self.assertEqual(response.data[1]['status'], 0)

    def test_question_flags_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(200, response.status_code)

        self.assertEqual(response.data['comments'][0]['user_id'], self.user.id)
        self.assertEqual(response.data['comments'][1]['user_id'], self.user2.id)
        self.assertEqual(response.data['comments'][2]['user_id'], self.user3.id)
        self.assertEqual(response.data['comments'][3]['user_id'], self.user4.id)

        self.assertEqual(response.data['comments'][0]['comment'], self.qflag.comment)
        self.assertEqual(response.data['comments'][1]['comment'], self.qflag2.comment)
        self.assertEqual(response.data['comments'][2]['comment'], self.qflag3.comment)
        self.assertEqual(response.data['comments'][3]['comment'], self.qflag4.comment)

    def test_question_flags_update(self):
        self.assertEqual(Post.objects.last().quarantine, False)
        self.assertEqual(QuestionFlag.objects.all()[0].status, 0)
        self.assertEqual(QuestionFlag.objects.all()[1].status, 0)
        self.assertEqual(QuestionFlag.objects.all()[2].status, 0)

        response = self.client.patch(self.detail_url, data={"status" : "2"}, content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(Post.objects.last().quarantine, True)
        self.assertEqual(QuestionFlag.objects.all()[0].status, 2)
        self.assertEqual(QuestionFlag.objects.all()[1].status, 2)
        self.assertEqual(QuestionFlag.objects.all()[2].status, 2)

    def test_question_flags_delete_only_qflags(self):
        self.assertEqual(QuestionFlag.objects.count(), 4)
        self.assertEqual(Post.objects.count(), 1)

        response = self.client.delete(self.detail_url)

        self.assertEqual(QuestionFlag.objects.count(), 0)
        self.assertEqual(Post.objects.count(), 1)

    def test_question_flags_delete_all(self):
        self.assertEqual(QuestionFlag.objects.count(), 4)
        self.assertEqual(Post.objects.count(), 1)

        self.client.patch(self.detail_url, data={"status" : "2"}, content_type='application/json')
        response = self.client.delete(self.detail_url)

        self.assertEqual(QuestionFlag.objects.count(), 0)
        self.assertEqual(Post.objects.count(), 0)
