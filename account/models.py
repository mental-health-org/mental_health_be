from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class MyAccountManager(BaseUserManager):

    def create_user(self, username, email, title, password):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have a email")
        if not title:
            raise ValueError("Users must have a title")
        user = self.model(
            username=username,
            email=self.normailze_email(email),
            title=title,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, title, password):
        user = self.create_user(
            username=username,
            email=self.normailze_email(email),
            title=title,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    connections = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_connection', through='Connection')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'title']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

# Generates Token for newly registered Users
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Connection(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 0, "pending"
        CONNECTED = 1, "connected"
        DISCONNECTED = 2, "disconnected"

    user_sent = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_sent', default=None, blank=True, on_delete=models.CASCADE)
    user_received = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_received', default=None, blank=True, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
