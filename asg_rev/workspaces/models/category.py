from django.db import models
from workspaces.models.workspace import Workspace  

class Category(models.Model):
    name = models.CharField(
        max_length=100,
    )
    workspace = models.ForeignKey(
        Workspace,  
        on_delete=models.CASCADE,  
        related_name='categories'  
    )

    def __str__(self):
        return self.name
