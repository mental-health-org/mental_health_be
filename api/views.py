from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from .serializers import *
from .models import *
from rest_framework import filters, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response as FinalResponse
from django.utils.decorators import method_decorator #tells django POST method does not need a CSRF token
from django.views.decorators.csrf import csrf_exempt #tells django POST method does not need a CSRF token
import json


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

@method_decorator(csrf_exempt, name='dispatch') #tells django POST method does not need a CSRF token
class MentalHealth(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        r_body = data.get('body')
        r_user = data.get('user')
        r_post = data.get('post')

        response_data = {
            'body': r_body,
            'user': User.objects.get(id=r_user),
            'post': Post.objects.get(id=r_post),
        }

        response = Response.objects.create(**response_data)

        data = {
            "message": f"New item added to Response with id: {response.id}"
        }
        return JsonResponse(data, status=201)
