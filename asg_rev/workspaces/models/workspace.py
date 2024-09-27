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
