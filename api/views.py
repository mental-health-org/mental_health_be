from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
<<<<<<< HEAD
from .serializers import *
from .models import *
from rest_framework import filters, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


@api_view(('GET',))
def question_search(request):

    if request.GET.get('search') == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    search = request.GET.get('search')
    title_results = Post.objects.filter(title__icontains=search)
    serializer = QuestionsSerializer(title_results, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(('GET',))
def question_tags_search(request):
    tags = request.GET.get('tags')

    if Tag.objects.filter(name=tags).first() == None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    results = Post.objects.filter(tagging__name=tags)
    serializer = QuestionsSerializer(results, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
=======
from .models import User, Post, Tag, Response
import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# def questions_list(request):

@method_decorator(csrf_exempt, name='dispatch')
class MentalHealth(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        r_body = data.get('body')
        r_user = data.get('user')
        r_post = data.get('post')

        response_data = {
            'body': r_body,
            'user': r_user,
            'post': r_post,
        }

        response = Response.objects.create(**response_data)

        data = {
            "message": f"New item added to Response with id: {response.id}"
        }
        return JsonResponse(data, status=201)
>>>>>>> ec8c2d0 (Setup post responses endpoint; not working)
