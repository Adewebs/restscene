from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.


class UserInfo(AbstractUser):
    is_user_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    forgetpass_token = models.CharField(max_length=255, blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        related_name='customer_groups',  # Add a unique related_name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customer_user_permissions',  # Add a unique related_name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    REQUIRED_FIELDS = []
