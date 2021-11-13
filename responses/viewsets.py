from rest_framework.response import Response as FinalResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework import viewsets, status
from django.http import HttpResponse
from django.http import Http404
from responses.serializers import *
from responses.models import *

User = get_user_model()

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

class ResponseFlagViewSet(viewsets.ViewSet):

        def list(self, request):
            # if request.user.is_superuser:
            queryset = ResponseFlag.objects.all().distinct('response')
            serializer = ListResponseFlagSerializer(queryset, many=True)
            return FinalResponse(serializer.data)
            # else:
            #     raise Http404

        def retrieve(self, request, pk=None):
            queryset = ResponseFlag.objects.all()
            flagged_response = get_object_or_404(queryset, pk=pk)
            serializer = DetailedResponseFlagSerializer(flagged_response)
            return FinalResponse(serializer.data)

        def partial_update(self, request, pk=None):
            rflag = ResponseFlag.objects.get(id = pk)
            queryset = ResponseFlag.objects.filter(response=rflag.response.id)

            for flag in queryset:
                flag.status = request.data['status']
                flag.save()

            if request.data['status'] == 0 | 1:
                obj = Response.objects.get(id=rflag.response.id)
                obj.quarantine = False
                obj.save()
            else:
                obj = Response.objects.get(id=rflag.response.id)
                obj.quarantine = True
                obj.save()

            return FinalResponse({"update":"Response and related flags have been updated"},status=status.HTTP_200_OK)

        def destroy(self, request, *args, **kwargs):
            rflag = ResponseFlag.objects.get(id = self.kwargs['pk'])
            queryset = ResponseFlag.objects.filter(response=rflag.response.id)

            if rflag.status == 2:
                response = Response.objects.get(id = rflag.response.id)
                self.perform_destroy(response)

            for flag in queryset:
                self.perform_destroy(flag)

            return FinalResponse(status=status.HTTP_204_NO_CONTENT)

        def perform_destroy(self, instance):
            instance.delete()

        def create(self, request):
            instance = ResponseFlag.objects.filter(response=request.data['response']).first()

            if instance == None:
                serializer = ResponseFlagSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                new_data = request.data.copy()
                new_data.update({'status' : instance.status})
                serializer = ResponseFlagSerializer(data=new_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            return FinalResponse(serializer.data, status=status.HTTP_201_CREATED)
