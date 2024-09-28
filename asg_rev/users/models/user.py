from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
  
class User(AbstractUser):
    AUTH_CHOICES = [
        ('email','Email'),
        ('google','Google'),
        ('channeli','Channeli')
    ]
    first_name = None
    last_name = None
    email = models.EmailField(
        max_length=250,
        unique=True,
        null=False,
        blank=False
        )
    profile_pic = models.URLField(
        max_length=250,
        blank=True,
    )
    auth_type = models.CharField(
        max_length=10,
        choices=AUTH_CHOICES,
        default='email'
    )


