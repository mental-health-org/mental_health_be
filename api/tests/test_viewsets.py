from django.test import TestCase
from api.models import *
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

class TestUsersViewSets(TestCase):
    def setUp(self):
        # Create Objects
        self.user = User.objects.create(username = 'Billy')

        # Get URL's
        self.detail_url = reverse("users-detail", args={self.user.id})
        self.detail_url_404 = reverse('users-detail', args={0})

    def test_users_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.user.username)

    def test_users_detail_404(self):
        response = self.client.get(self.detail_url_404)
        self.assertEqual(response.status_code, 404)

    def test_users_create(self):
        self.assertEqual(1, len(User.objects.all()))

        response = self.client.post("/api/v1/users/",{"username": "Good User"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(2, len(User.objects.all()))

    def test_users_create_400(self):

        response = self.client.post("/api/v1/users/",{"invalid": 2})
        self.assertEqual(response.status_code, 400)

    def test_delete_user(self):
        response = self.client.delete("/api/v1/users/"+str(self.user.id)+"/", content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.all().count(), 0)

    def test_users_patch(self):
        old_username = User.objects.last().username
        response = self.client.patch("/api/v1/users/"+str(self.user.id)+"/", data={"username": "gooduser"}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(User.objects.last().username, old_username)


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

    # def test_response_create_404(self):
    #
    #     response = self.client.post("/api/v1/responses/",{"post": "1000", "body": "that post id does not exist"})
    #     self.assertEqual(response.status_code, 404)

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

    # def test_question_votes_create_403(self):
    #
    #     response = self.client.post("/api/v1/qvote/", {"user": , "post": str(self.post.id), "vote_type": "1"})
    #     self.assertEqual(response.status_code, 403)

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

    # def test_response_votes_create_403(self):
    #
    #     response = self.client.post("/api/v1/qvote/", {"response1": str(self.response1.id), "vote_type": "1"})
    #     self.assertEqual(response.status_code, 403)
