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

