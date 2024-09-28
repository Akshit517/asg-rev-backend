import uuid
from django.db import models
from workspaces.models.category import Category

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
    #assignment = models.ForeignKey()

from users.models.user import User
from users.models.role import Role

class ChannelRole(models.Model):
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
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='channel_role'
    )
    class Meta:
        unique_together = ('user', 'channel', 'role')  

    def __str__(self):
        return f"{self.user} - {self.role} in {self.channel}"