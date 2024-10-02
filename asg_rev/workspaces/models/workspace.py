import uuid
from django.db import models
from users.models.user import User

class Workspace(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=50,
    )
    icon = models.URLField(
        max_length=250,
    ) 
    owner = models.ForeignKey(
        User,  
        on_delete=models.CASCADE,  
        related_name='workspaces'  
    )
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name


class WorkspaceRole(models.Model):
    ROLE_CHOICES = [
        ('workspace_admin', 'Workspace_Admin'),
        ('workspace_member', 'Workspace_Member')
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workspace_role'
    )
    workspace = models.ForeignKey(
        Workspace,  
        on_delete=models.CASCADE,  
        related_name='workspace_role'  
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='workspace_member',
        blank=False
    )
    
    class Meta:
        unique_together = ('user', 'workspace')  

    def __str__(self):
        return f"{self.user} - {self.role} in {self.workspace}"
