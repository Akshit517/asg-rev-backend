from django.db import models
from users.models import User
import uuid

class PrivateChat(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    participants = models.ManyToManyField(
        User, 
        related_name='private_chats'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Private chat between {' and '.join([user.username for user in self.participants.all()])}"
