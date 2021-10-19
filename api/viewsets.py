from .models import User, Post, Tag
from django.shortcuts import get_object_or_404
from .serializers import QuestionsSerializer
from rest_framework import viewsets
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
