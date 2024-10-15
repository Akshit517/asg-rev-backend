import uuid
from django.db import models
from workspaces.models.category import Category
from users.models.user import User

class Channel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=50,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='channel'
    )

class ChannelRole(models.Model):
    ROLE_CHOICES = [
        ('reviewer', 'Reviewer'),
        ('reviewee', 'Reviewee')
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='channel_role'
    )
    channel = models.ForeignKey(
        Channel,  
        on_delete=models.CASCADE,  
        related_name='channel_role'  
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='reviewer',
        blank=False
    )

    class Meta:
        unique_together = ('user', 'channel')  

    def save(self, *args, **kwargs):
        if self.role not in dict(self.ROLE_CHOICES).keys():
            raise ValueError(f"Role must be one of: {', '.join(dict(self.ROLE_CHOICES).keys())}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.role} in {self.channel}"