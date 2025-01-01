from django.db.models.signals import post_save
from django.dispatch import receiver

from workspaces.models.category import (
    Category,
    CategoryRole,
)
from workspaces import utils

@receiver(post_save, sender=Category)
def create_rolecategory(sender, created, instance, **kwargs):
    if created: 
        user = utils.get_current_user_or_none()
        if user is not None:
            role = 'category_admin'
            CategoryRole.objects.create(
                user=user,
                category=instance,
                role=role
            )