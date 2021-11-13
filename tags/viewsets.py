from rest_framework.response import Response as FinalResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status
from django.http import HttpResponse
from django.http import Http404
from tags.serializers import *
from tags.models import *

class TagsViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Tag.objects.all()
        serializer = tags_serializer(queryset)
        return FinalResponse(serializer)

    def retrieve(self, request, pk=None):
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        serializer = TagsSerializer(tag)
        return FinalResponse(serializer.data)

def tags_serializer(queryset):
    all_tags = []
    for tag in queryset:
        all_tags.append(tag.name)
    return {"id": None, "type": "tags", "attributes" : all_tags}
