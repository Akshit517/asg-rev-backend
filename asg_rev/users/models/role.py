from django.contrib.auth.models import Permission
from django.db import models

class Role(models.Model):
    ROLE_LEVEL_CHOICES = (
        ('workspace', 'Workspace'),
        ('category', 'Category'),
        ('channel', 'Channel'),
    )
    
    role_title = models.CharField(
        max_length=20,
        unique=True,
    )
    role_level = models.CharField(
        max_length=15,
        choices=ROLE_LEVEL_CHOICES,
        default='channel'
    )
    permissions = models.ManyToManyField(Permission, blank=True)
    
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"  

    def __str__(self):
        return self.role_title
