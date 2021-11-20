from .models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .serializers import *
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response as FinalResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.http import Http404

class AuthorizedUserViewSet(viewsets.ViewSet):

    def create(self, request):
        try:
            instance = Token.objects.get(key = request.data['token'])
            serializer = UserSerializer(instance.user)
            return FinalResponse(serializer.data)
        except:
            raise Http404

class UsersViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return FinalResponse(serializer.data)

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

class RegisterViewSet(viewsets.ViewSet):

    def create(self, request):
        data = {}
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        data['response'] = "Registration Successful"
        data['id'] = user.id
        data['username'] = user.username
        data['token'] = Token.objects.get(user=user).key

        return FinalResponse(data, status=status.HTTP_201_CREATED)

class LoginViewSet(viewsets.ViewSet):

    def create(self, request):
        data = {}
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            data['response'] = "Successful Login"
            data['token'] = Token.objects.get(user=user).key
            login(request, user)
            return FinalResponse(data, status=status.HTTP_200_OK)
        else:
            return FinalResponse({"Unable to log in with provided credentials."}, status=status.HTTP_400_BAD_REQUEST)

class LogoutViewSet(viewsets.ViewSet):

    def create(self, request):
        data = {}
        data['response'] = "Successfully Logged Out"
        logout(request)
        return FinalResponse(data, status=status.HTTP_200_OK)

class ConnectionViewSet(viewsets.ViewSet):

    def create(self, request):
        sent = User.objects.get(id=request.data["user_sent"])
        received = User.objects.get(id=request.data["user_received"])

        connection = Connection.objects.filter(user_sent = sent.id, user_received = received.id)
        if connection.first() == None:
            Connection.objects.create(user_sent = sent, user_received = received, status = 0)
            return FinalResponse("Connection Requested", status=status.HTTP_201_CREATED)

        connection.update(status = request.data["status"])
        return FinalResponse("Connection Made", status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = Connection.objects.filter(id=self.kwargs['pk'])
        self.perform_destroy(instance)
        return FinalResponse(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

# class AccountAuthBackend(object):
#
#     @staticmethod
#     def authenticate(email=None, password=None):
#         import pdb; pdb.set_trace()
#         try:
#             user = User.objects.get(email=email)
#             if user.check_password(password):
#                 return user
#         except User.DoesNotExist:
#             return None
#
#     @staticmethod
#     def get_user(id_):
#         try:
#             return User.objects.get(pk=id_)
#         except User.DoesNotExist:
#             return None
