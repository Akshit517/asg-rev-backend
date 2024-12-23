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
    description = models.TextField()
    for_teams = models.BooleanField(
        default=False
    ) 
    created_at = models.DateTimeField(
        auto_now_add=True
    ) 
    total_points = models.IntegerField()

    def __str__(self):
        return f'{self.id.name} -> {self.id.id}' 

class Task(models.Model):
    assignment = models.ForeignKey(
        Assignment, 
        on_delete=models.CASCADE, 
        related_name='tasks')
    task = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return self.task_name

