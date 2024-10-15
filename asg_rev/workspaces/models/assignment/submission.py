from django.db import models
from django.conf import settings
from workspaces import utils
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
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    content = models.TextField(
        blank=True, 
        null=True
    )
    file = models.FileField(
        upload_to=utils.submissions_file_path,
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
    team_leader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='team_leader'
    )
    members = models.ManyToManyField(
        User,
        related_name='team_members'
    )
    team_name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return f"{self.team_name} (Leader: {self.team_leader.username})"

class EarnedPoint(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE
    )
    reviewee = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    reviewee_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )
    earned_points = models.IntegerField()

    def __str__(self):
        if reviewee is None:
            return f'{self.assignment} -> {self.reviewee_team} = {self.earned_points}'

        return f'{self.assignment} -> {self.reviewee_team} = {self.earned_points}'    