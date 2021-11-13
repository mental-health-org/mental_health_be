from django.test import TestCase
from api.models import *
from account.models import *
from django.urls import reverse
from django.test.client import RequestFactory
import json

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


class TestTagsViewSets(TestCase):

    def setUp(self):
        # Create Objects
        self.tag = Tag.objects.create(name = 'addiction')
        self.tag2 = Tag.objects.create(name = 'child therapy')
        self.new_tags = ['therapy', 'anxiety']

        # Get URL's
        self.list_url = reverse('tags-list')
        self.detail_url = reverse('tags-detail', args={self.tag2.id})
        self.detail_url_404 = reverse('tags-detail', args={0})

    def test_tags_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["attributes"]), 2)

    def test_tags_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.tag2.id)
        self.assertEqual(response.data['name'], self.tag2.name)

    def test_tags_detail_404(self):
        response = self.client.get(self.detail_url_404)
        self.assertEqual(response.status_code, 404)

class TestResponsesViewSets(TestCase):
    def setUp(self):
        # Create Objects
        self.user = User.objects.create(username = 'Billy')
        self.post = Post.objects.create(title = 'Test Title', body = 'ipsum lorem')
        self.response = Response.objects.create(post_id = str(self.post.id), body = 'thing 1')
        self.response2 = Response.objects.create(post_id = str(self.post.id), body = 'thing 2 say')
        self.response3 = Response.objects.create(post_id = str(self.post.id), body = 'thing 3')

        # Get URL's
        self.detail_url = reverse("responses-detail", args={self.response.id})
        self.detail_url_404 = reverse('responses-detail', args={0})

    def test_response_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['body'], self.response.body)

    def test_response_detail_404(self):
        response = self.client.get(self.detail_url_404)
        self.assertEqual(response.status_code, 404)

    def test_response_create(self):
        self.assertEqual(3, len(Response.objects.all()))

        response = self.client.post("/api/v1/responses/",{ "user" : "", "post": str(self.post.id),"body": "Good Response" })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(4, len(Response.objects.all()))
        self.assertEqual("Good Response", self.post.response_set.last().body)

    def test_response_create_400(self):

        response = self.client.post("/api/v1/responses/",{"invalid": 2})
        self.assertEqual(response.status_code, 400)

    def test_response_patch(self):
        old_body = Response.objects.last().body
        response = self.client.patch("/api/v1/responses/"+str(self.response3.id)+"/", data={"body": "patch"}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(Response.objects.last().body, old_body)

    def test_response_delete(self):
        response = self.client.delete("/api/v1/responses/"+str(self.response.id)+"/", content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Response.objects.all().count(), 2)

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

class TestResponseVoteViewSet(TestCase):

    def setUp(self):
        # Create Objects
        self.user = User.objects.create(username = 'Orson Wells')
        self.post = Post.objects.create( user = self.user, title = 'Test Title', body = 'ipsum lorem')
        self.response1 = Response.objects.create( user = self.user, post = self.post, body = 'ipsum lorem')

    def test_response_votes_create(self):
        response = self.client.post("/api/v1/rvote/", {"user": str(self.user.id), "response": str(self.response1.id), "vote_type": "1"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(1, len(ResponseVote.objects.all()))
        self.assertEqual(1, ResponseVote.objects.first().vote_type)

        # Vote type can be changed to downvote
        response = self.client.post("/api/v1/rvote/", {"user": str(self.user.id), "response": str(self.response1.id), "vote_type": "2"})
        self.assertEqual(1, len(ResponseVote.objects.all()))
        self.assertEqual(2, ResponseVote.objects.first().vote_type)

        # Vote type can be changed to novote
        response = self.client.post("/api/v1/rvote/", {"user": str(self.user.id), "response": str(self.response1.id), "vote_type": "2"})
        self.assertEqual(1, len(ResponseVote.objects.all()))
        self.assertEqual(3, ResponseVote.objects.first().vote_type)

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


class TestResponseFlagVoteViewSet(TestCase):

    def setUp(self):
        # Create Objects
        self.user = User.objects.create(username = 'Orson Wells')
        self.admin_user = User.objects.create(username = 'Admin', email = 'admin@admin.email',is_admin = True)
        self.post = Post.objects.create( user = self.user, title = 'Test Title', body = 'ipsum lorem')
        self.response = Response.objects.create( user = self.user, post = self.post, body = 'ipsum lorem')
        self.rflag = ResponseFlag.objects.create(user = self.user, response = self.response, comment = "bad answer")

        self.user2 = User.objects.create(username = 'Second_User', email = '1@email.com')
        self.user3 = User.objects.create(username = 'Third_User', email = '2@email.com')
        self.user4 = User.objects.create(username = 'Fourth_User', email = '3@email.com')

        self.rflag2 = ResponseFlag.objects.create(user = self.user2, response = self.response, comment = "second flag")
        self.rflag3 = ResponseFlag.objects.create(user = self.user3, response = self.response, comment = "third flag")
        self.rflag4 = ResponseFlag.objects.create(user = self.user4, response = self.response, comment = "fourth flag")

        # Get URL's
        self.list_url = reverse('rflag-list')
        self.detail_url = reverse('rflag-detail', args = {str(self.rflag.id)})

        self.request_factory = RequestFactory()

    def test_response_flags_create(self):
        response = self.client.post(self.list_url, {"user": str(self.user.id), "response": str(self.response.id), "comment": "bad response"})
        self.assertEqual(5, ResponseFlag.objects.count())
        self.assertEqual(201, response.status_code)

    def test_response_flags_create_no_starting_items(self):
        ResponseFlag.objects.all().delete()
        response = self.client.post(self.list_url, {"user": str(self.user.id), "response": str(self.response.id), "comment": "bad response"})
        self.assertEqual(1, ResponseFlag.objects.count())
        self.assertEqual(201, response.status_code)

    def test_response_flags_list(self):
        self.response2 = Response.objects.create( user = self.user, post = self.post, body = 'ipsum lorem')
        rflag5 = ResponseFlag.objects.create(user = self.user, response = self.response2, comment = "this is a second response")

        response = self.client.get(self.list_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data[0]['response'], self.response.id)
        self.assertEqual(response.data[0]['status'], 0)
        self.assertEqual(response.data[1]['response'], self.response2.id)
        self.assertEqual(response.data[1]['status'], 0)

    def test_response_flags_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(200, response.status_code)

        self.assertEqual(response.data['comments'][0]['user_id'], self.user.id)
        self.assertEqual(response.data['comments'][1]['user_id'], self.user2.id)
        self.assertEqual(response.data['comments'][2]['user_id'], self.user3.id)
        self.assertEqual(response.data['comments'][3]['user_id'], self.user4.id)

        self.assertEqual(response.data['comments'][0]['comment'], self.rflag.comment)
        self.assertEqual(response.data['comments'][1]['comment'], self.rflag2.comment)
        self.assertEqual(response.data['comments'][2]['comment'], self.rflag3.comment)
        self.assertEqual(response.data['comments'][3]['comment'], self.rflag4.comment)

    def test_response_flags_update(self):
        self.assertEqual(Response.objects.last().quarantine, False)
        self.assertEqual(ResponseFlag.objects.all()[0].status, 0)
        self.assertEqual(ResponseFlag.objects.all()[1].status, 0)
        self.assertEqual(ResponseFlag.objects.all()[2].status, 0)

        response = self.client.patch(self.detail_url, data={"status" : "2"}, content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(Response.objects.last().quarantine, True)
        self.assertEqual(ResponseFlag.objects.all()[0].status, 2)
        self.assertEqual(ResponseFlag.objects.all()[1].status, 2)
        self.assertEqual(ResponseFlag.objects.all()[2].status, 2)

    def test_response_flags_delete_only_rflags(self):
        self.assertEqual(ResponseFlag.objects.count(), 4)
        self.assertEqual(Response.objects.count(), 1)

        response = self.client.delete(self.detail_url)

        self.assertEqual(ResponseFlag.objects.count(), 0)
        self.assertEqual(Response.objects.count(), 1)

