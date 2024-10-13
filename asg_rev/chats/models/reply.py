from django.db import models
from chats.models import (
    Message,
)
from users.models import (
    User,
)

class Reply(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='replies_message'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='replies_user'
    )
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )  

    def __str__(self):
        return f'Reply from {self.user.username} to {self.message.id}'
    