from .models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .serializers import *
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response as FinalResponse

class QuestionsViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Post.objects.all()
        serializer = QuestionsSerializer(queryset, many=True)
        return FinalResponse(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        question = get_object_or_404(queryset, pk=pk)
        serializer = SingleQuestionSerializer(question)
        return FinalResponse(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = Post.objects.filter(id=self.kwargs['pk'])
        self.perform_destroy(instance)
        return FinalResponse(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def partial_update(self, request, pk=None):
        queryset = Post.objects.all()
        question = get_object_or_404(queryset, pk=pk)
        serializer = QuestionsSerializer(question, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return FinalResponse(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        tags_data = request.data.copy().pop('tags')
        post_data = request.data.copy()
        del post_data['tags']

        serializer = PostSerializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        new_post = Post.objects.filter(title=post_data['title']).last()

        formatted_tags = []
        for tag in tags_data:
            formatted_tags.append(tag.strip().lower().title())

        for tag in formatted_tags:
            if not Tag.objects.filter(name=tag):
                new_tag = Tag.objects.create(name=tag)
                new_post.tagging.add(new_tag.id)
            else:
                existing_tag = Tag.objects.filter(name=tag).last()
                new_post.tagging.add(existing_tag.id)

        response =  header_serializer('questions', {'question': serializer.data, 'tags': formatted_tags})

        return FinalResponse(response, status=status.HTTP_201_CREATED)

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

class PostsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return FinalResponse(serializer.data)

class UsersViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return FinalResponse(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return FinalResponse(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        queryset = User.objects.all()
        response = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(response, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return FinalResponse(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = User.objects.filter(id=self.kwargs['pk'])
        self.perform_destroy(instance)
        return FinalResponse(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class ResponsesViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = Response.objects.all()
        response = get_object_or_404(queryset, pk=pk)
        serializer = ResponseSerializer(response)
        return FinalResponse(serializer.data)

    def create(self, request):
        serializer = ResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return FinalResponse(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        queryset = Response.objects.all()
        response = get_object_or_404(queryset, pk=pk)
        serializer = ResponseSerializer(response, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return FinalResponse(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = Response.objects.filter(id=self.kwargs['pk'])
        self.perform_destroy(instance)
        return FinalResponse(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
