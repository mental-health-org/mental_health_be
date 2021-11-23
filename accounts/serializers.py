from django.core import serializers as core_serializers
from rest_framework import serializers
from django.db.models import Q
from .models import *

class UserSerializer(serializers.ModelSerializer):
    connections = serializers.SerializerMethodField()

    def get_connections(self, obj):
        connected = []
        pending = []
        requested = Connection.objects.filter(user_received = obj.id, status=0)
        accepted = Connection.objects.filter(Q(user_received = obj.id, status=1) | Q(user_sent = obj.id, status=1))

        for request in requested:
            pending.append({"id":request.id, "name":request.user_sent.username})
        for linked in accepted:
            if linked.user_sent.id != obj.id:
                connected.append({"id":linked.id, "name":linked.user_sent.username})
            elif linked.user_received != obj.id:
                connected.append({"id":linked.id, "name":linked.user_received.username})

        return {"connected": connected, "pending": pending}

    class Meta:
        model = User
        fields = ("id", "username", "title",
        "email", "is_active", "is_admin", "is_staff", "is_superuser",
        "connections", "last_login", "created_at", "updated_at")

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'title', 'email', 'password', 'password2']
        extra_kwargs = {
                    'password': {'write_only': True}
        }

    # Save override to ensure both passwords match
    def save(self):
        user = User(
                username = self.validated_data['username'],
                email = self.validated_data['email'],
                title = self.validated_data['title'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user

        
