from django.test import TestCase
from api.models import User, Post, Tag
from django.urls import reverse
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

class TestTagsViewSets(TestCase):

    def setUp(self):
        # Create Objects
        self.tag = Tag.objects.create(name = 'addiction')
        self.tag2 = Tag.objects.create(name = 'child therapy')

        # Get URL's
        self.list_url = reverse('tags-list')
        self.detail_url = reverse('tags-detail', args={self.tag2.id})
        self.detail_url_404 = reverse('tags-detail', args={0})

    def test_tags_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_tags_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.tag2.id)
        self.assertEqual(response.data['name'], self.tag2.name)

    def test_tags_detail_404(self):
        response = self.client.get(self.detail_url_404)
        self.assertEqual(response.status_code, 404)
