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

from users.models.user import User
from users.models.role import Role

class CategoryRole(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='category_role'
    )
    category = models.ForeignKey(
        Category,  
        on_delete=models.CASCADE,  
        related_name='category_role'  
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='category_role'
    )
    class Meta:
        unique_together = ('user', 'category', 'role')  

    def __str__(self):
        return f"{self.user} - {self.role} in {self.category}"