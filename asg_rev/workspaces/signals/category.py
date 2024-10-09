from django.db.models.signals import post_save
from django.dispatch import receiver

from workspaces.models.category import (
    Category,
    CategoryRole,
)
from users.models.user import User

from crum import get_current_user

def get_current_user_or_none():
    u = get_current_user()
    if not isinstance(u, User):
        return None
    return u

@receiver(post_save, sender=Category)
def create_rolecategory(sender, created, instance, **kwargs):
    if created: 
        user = get_current_user_or_none()
        if user is not None:
            role = 'category_admin'
            CategoryRole.objects.create(
                user=user,
                category=instance,
                role=role
            )