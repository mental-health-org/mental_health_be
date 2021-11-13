from django.core import serializers as core_serializers
from rest_framework import serializers
from tags.models import *

class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')
