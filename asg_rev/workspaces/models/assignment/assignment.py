from django.db import models
from workspaces.models import Channel 
from users.models import User 

class Assignment(models.Model):
    id = models.OneToOneField(
        Channel, 
        on_delete=models.CASCADE, 
        related_name='assignment',
        primary_key=True
    )
    description = models.CharField(
        max_length=255
    )
    for_teams = models.BooleanField(
        default=False
    ) 
    created_at = models.DateTimeField(
        auto_now_add=True
    ) 
    total_points = models.IntegerField()

    def __str__(self):
        return self.title.name

class Task(models.Model):
    assignment = models.ForeignKey(
        Assignment, 
        on_delete=models.CASCADE, 
        related_name='tasks')
    task = models.CharField(
        max_length=255
    )
    due_date = models.DateTimeField()

    def __str__(self):
        return self.task_name

class Team(models.Model):
    team_name = models.CharField(
        max_length=100
    ) 
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='teams'
    )
    team_leader = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='team_leader'
    )
    members = models.ManyToManyField(
        User,
        related_name='team_members'
    )
    points_earned = models.IntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.team_name} (Leader: {self.team_leader.username})"

