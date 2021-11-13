from .models import *
from account.models import *
from django.http import Http404
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

class QuestionVoteViewSet(viewsets.ViewSet):

    def create(self, request):
        post_obj = Post.objects.get(id=request.data["post"])
        user_obj = User.objects.get(id=request.data["user"])

        vote = QuestionVotes.objects.filter(user = user_obj.id, post=post_obj.id)
        if vote.first() == None:
            QuestionVotes.objects.create(post = post_obj, user = user_obj, vote_type = request.data["vote_type"])
            return FinalResponse("vote updated", status=status.HTTP_201_CREATED)

        if vote.first().vote_type == int(request.data["vote_type"]):
            vote.update(vote_type = 3)
            return FinalResponse("vote updated", status=status.HTTP_201_CREATED)

        vote.update(vote_type = int(request.data["vote_type"]))
        return FinalResponse("vote updated", status=status.HTTP_201_CREATED)

class ResponseVoteViewSet(viewsets.ViewSet):

    def create(self, request):
        response_obj = Response.objects.get(id=request.data["response"])
        user_obj = User.objects.get(id=request.data["user"])

        vote = ResponseVote.objects.filter(user = user_obj.id, response=response_obj.id)
        if vote.first() == None:
            ResponseVote.objects.create(response = response_obj, user = user_obj, vote_type = request.data["vote_type"])
            return FinalResponse("vote updated", status=status.HTTP_201_CREATED)

        if vote.first().vote_type == int(request.data["vote_type"]):
            vote.update(vote_type = 3)
            return FinalResponse("vote updated", status=status.HTTP_201_CREATED)

        vote.update(vote_type = int(request.data["vote_type"]))
        return FinalResponse("vote updated", status=status.HTTP_201_CREATED)

class QuestionFlagViewSet(viewsets.ViewSet):

    def list(self, request):
        # if request.user.is_superuser:
        queryset = QuestionFlag.objects.all().distinct('post')
        serializer = ListQuestionFlagSerializer(queryset, many=True)
        return FinalResponse(serializer.data)
        # else:
        #     raise Http404

    def retrieve(self, request, pk=None):
        queryset = QuestionFlag.objects.all()
        flagged_question = get_object_or_404(queryset, pk=pk)
        serializer = DetailedQuestionFlagSerializer(flagged_question)
        return FinalResponse(serializer.data)

    def partial_update(self, request, pk=None):
        qflag = QuestionFlag.objects.get(id = pk)
        queryset = QuestionFlag.objects.filter(post=qflag.post.id)

        for flag in queryset:
            flag.status = request.data['status']
            flag.save()

        if request.data['status'] == 0 | 1:
            obj = Post.objects.get(id=qflag.post.id)
            obj.quarantine = False
            obj.save()
        else:
            obj = Post.objects.get(id=qflag.post.id)
            obj.quarantine = True
            obj.save()

        return FinalResponse({"update":"Question and related flags have been updated"},status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        qflag = QuestionFlag.objects.get(id = self.kwargs['pk'])
        queryset = QuestionFlag.objects.filter(post=qflag.post.id)

        if qflag.status == 2:
            question = Post.objects.get(id = qflag.post.id)
            self.perform_destroy(question)

        for flag in queryset:
            self.perform_destroy(flag)

        return FinalResponse(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def create(self, request):
        instance = QuestionFlag.objects.filter(post=request.data['post']).first()

        if instance == None:
            serializer = QuestionFlagSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            new_data = request.data.copy()
            new_data.update({'status' : instance.status})
            serializer = QuestionFlagSerializer(data=new_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return FinalResponse(serializer.data, status=status.HTTP_201_CREATED)


