from uuid import uuid4

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=timezone.now(),
            registered_at=timezone.now(),
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        is_staff = extra_fields.pop('is_staff', False)
        is_superuser = extra_fields.pop('is_superuser', False)
        return self._create_user(username, email, password, is_staff, is_superuser, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, is_staff=True, is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='Username', unique=True, max_length=64)
    email = models.EmailField(verbose_name='Email', unique=True, max_length=255)
    first_name = models.CharField(verbose_name='First name', max_length=30, default='first')
    last_name = models.CharField(verbose_name='Last name', max_length=30, default='last')
    avatar = models.ImageField(verbose_name='Avatar', blank=True)
    token = models.UUIDField(verbose_name='Token', default=uuid4, editable=False)

    is_admin = models.BooleanField(verbose_name='Admin', default=False)
    is_active = models.BooleanField(verbose_name='Active', default=True)
    is_staff = models.BooleanField(verbose_name='Staff', default=False)
    registered_at = models.DateTimeField(verbose_name='Registered at', auto_now=True)

    # Fields settings
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    full_name.fget.short_description = 'Full name'

    @property
    def short_name(self):
        return f'{self.last_name} {self.first_name[0]}.'
    short_name.fget.short_description = 'Short name'

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.short_name

    def get_blogs(self):
        return self.blogs.all()

    def get_orders(self):
        return self.orders.all()

    def __str__(self):
        return self.full_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
