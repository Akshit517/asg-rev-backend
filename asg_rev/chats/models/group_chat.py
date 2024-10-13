from django.db import models
from workspaces.models import (
    Channel,
    ChannelRole,
)
from users.models import User

class GroupChat(models.Model):
    channel = models.OneToOneField(
        Channel,
        primary_key=True,
        on_delete=models.CASCADE,
    )
    members = models.ManyToManyField(
        User, 
        related_name='group_chats'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        for member in self.members.all():
            if not ChannelRole.objects.filter(channel=self.channel, user=member).exists():
                raise ValidationError(f"{member.username} is not member of {self.channel.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"GroupChat in {self.channel.name}"