from django.test import TestCase
from api.models import *
from api.serializers import *

class TestTagsSerializer(TestCase):

    def setUp(self):
        self.tag_attributes = {"name": "Help"}

        self.tag = Tag.objects.create(**self.tag_attributes)
        self.serializer = TagsSerializer(instance=self.tag)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(["id", "name"]))

