from django.db import models
from users.models import User
from chats.models import (
    GroupChat,
    PrivateChat,
)

class Message(models.Model):
    sender = models.ForeignKey(
        User, 
        related_name='sender_messages', 
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    is_group = models.BooleanField(
        default=False
    )
    group_chat = models.ForeignKey(
        GroupChat, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    private_chat = models.ForeignKey(
        'PrivateChat', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender} at {self.created_at}"