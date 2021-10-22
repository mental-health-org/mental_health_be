from .models import User, Post, Tag
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .serializers import QuestionsSerializer, TagsSerializer, PostSerializer
from .serializers import basic_serializer
from rest_framework import viewsets, status
from rest_framework.response import Response

class QuestionsViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Post.objects.all()
        serializer = QuestionsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        question = get_object_or_404(queryset, pk=pk)
        serializer = QuestionsSerializer(question)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = Post.objects.filter(id=self.kwargs['pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def create(self, request):
        tags_data = request.data.copy().pop('tags')
        post_data = request.data.copy()
        del post_data['tags']

        post_serializer = PostSerializer(data=post_data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        new_post = Post.objects.filter(title=post_data['title']).last()

        for tag in tags_data:
            if not Tag.objects.filter(name=tag):
                new_tag = Tag.objects.create(name=tag)
                new_post.tagging.add(new_tag.id)
            else:
                existing_tag = Tag.objects.filter(name=tag).last()
                new_post.tagging.add(existing_tag.id)

        response =  {
                    'id': None, 'type': 'questions', 'attributes':
                    {'question': post_serializer.data, 'tags': tags_data}
        }

        return Response(response, status=status.HTTP_201_CREATED)

class TagsViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Tag.objects.all()
        serializer = TagsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        serializer = TagsSerializer(tag)
        return Response(serializer.data)

class PostsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
