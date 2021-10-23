from django.test import TestCase
from api.models import *
from django.urls import reverse
from django.test.client import RequestFactory
import json

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
