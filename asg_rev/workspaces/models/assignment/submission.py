from django.db import models
from workspaces.models import (
    Assignment,
)
from users.models import (
    User,
)

class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    file = models.FileField(
        upload_to='submissions/'
    )
    content = models.TextField(
        blank=True, 
        null=True
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    sent = models.DateTimeField(
        auto_now_add=True
    )
    
    def __str__(self):
        return f"Submission by {self.sender} for {self.assignment}"
    
    def clean(self):
        if self.file is None and self.content is None:
            raise ValidationError(_('File or Content should not be null'))