from django.db import models
from users.models.user import User
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

class CategoryRole(models.Model):
    ROLE_CHOICES = [
        ('category_admin', 'Category_Admin'),
        ('category_member', 'Category_Member')
    ]
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
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='category_member',
        blank=False
    )
    
    class Meta:
        unique_together = ('user', 'category') 

    def save(self, *args, **kwargs):
        if self.role not in dict(self.ROLE_CHOICES).keys():
            raise ValueError(f"Role must be one of: {', '.join(dict(self.ROLE_CHOICES).keys())}")
        super().save(*args, **kwargs) 

    def __str__(self):
        return f"{self.user} - {self.role} in {self.category}"