from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response as FinalResponse
from rest_framework import filters, generics, status
from rest_framework.decorators import api_view
from questions.serializers import *
from django.views import View
from questions.models import *

@api_view(('GET',))
def question_search(request):

    if request.GET.get('search') == None:
        return FinalResponse(status=status.HTTP_400_BAD_REQUEST)

    search = request.GET.get('search')
    title_results = Post.objects.filter(title__icontains=search)
    serializer = QuestionsSerializer(title_results, many=True)
    return FinalResponse(serializer.data, status=status.HTTP_200_OK)

@api_view(('GET',))
def question_tags_search(request):
    tags = request.GET.get('tags')

    if Tag.objects.filter(name=tags).first() == None:
        return FinalResponse(status=status.HTTP_404_NOT_FOUND)

    results = Post.objects.filter(tagging__name=tags)
    serializer = QuestionsSerializer(results, many=True)
    return FinalResponse(serializer.data, status=status.HTTP_200_OK)

def format_tags(tags_data):
    formatted_tags = []
    for tag in tags_data:
        if not tag.strip():
            pass
        else:
            formatted_tags.append(tag.strip().lower().title())
    return formatted_tags

