from django.db import models
from django.conf import settings
from workspaces import utils
from workspaces.models.assignment.assignment import (
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
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    content = models.TextField(
        blank=True, 
        null=True
    )
    file = models.URLField(
        null=True
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True
    )
    
    def __str__(self):
        return f"Submission by {self.sender} for {self.assignment}"
    
    def clean(self):
        if self.file is None and self.content is None:
            raise ValidationError(_('File or Content should not be null'))

class Team(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='teams'
    )
    members = models.ManyToManyField(
        User,
        related_name='team_members'
    )
    team_name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return f"{self.team_name}"
