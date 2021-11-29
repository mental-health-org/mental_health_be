from django.test.client import RequestFactory
from django.test import TestCase
from questions.models import *
from django.urls import reverse
from questions.views import *

class TestSearchFunctions(TestCase):

    def setUp(self):
    # Create Objects
        self.post = Post.objects.create( title = 'Test Title', body = 'ipsum lorem' )
        self.post2 = Post.objects.create( title = 'Test Two', body = 'body 2')
        self.tag = Tag.objects.create( name = "Anxiety" )
        self.tag2 = Tag.objects.create( name = "Depression" )
        self.post.tagging.add(self.tag)
        self.post2.tagging.add(self.tag2)

    # Get URL's
        self.question_url = reverse('search_questions')
        self.filter_url = reverse('filter_questions')

    def test_question_search(self):
        response = self.client.get(self.question_url+"?search=tle")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.post.id)

    def test_question_search_returns_empty(self):
        response = self.client.get(self.question_url+"?search=Does+Not+Exist")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_question_search_400(self):
        response = self.client.get(self.question_url+"?nothing=Does+Not+Exist")
        self.assertEqual(response.status_code, 400)

    def test_question_filter(self):
        response = self.client.get(self.filter_url+"?tags=Depression")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.post2.id)

    def test_question_filter_404(self):
        response = self.client.get(self.filter_url+"?tags=Does+Not+Exist")
        self.assertEqual(response.status_code, 404)

    def test_question_filter_400(self):
        response = self.client.get(self.question_url+"?nothing=Does+Not+Exist")
        self.assertEqual(response.status_code, 400)

class TestTagMethods(TestCase):

    def setUp(self):
        self.tags = ["  TaG ONe  ", "TAG TWO", "tag three"]
        self.tags_empty = ["  TesT Tag 1  ", "   ", "", "" ]
        self.formatted_tags = ["Tag One", "Tag Two", "Tag Three"]

    def test_formatting_tags(self):
        formatted = format_tags(self.tags)
        self.assertEqual(formatted[0], self.formatted_tags[0])
        self.assertEqual(formatted[1], self.formatted_tags[1])
        self.assertEqual(formatted[2], self.formatted_tags[2])

