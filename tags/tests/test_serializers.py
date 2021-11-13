from django.test import TestCase
from tags.serializers import *
from tags.models import *

class TestTagsSerializer(TestCase):

    def setUp(self):
        self.tag_attributes = {"name": "Help"}

        self.tag = Tag.objects.create(**self.tag_attributes)
        self.serializer = TagsSerializer(instance=self.tag)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(["id", "name"]))

    def test_name_field(self):
        data = self.serializer.data

        self.assertEqual(data['name'], self.tag_attributes['name'])
