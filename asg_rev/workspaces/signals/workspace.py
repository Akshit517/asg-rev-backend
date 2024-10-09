from django.db.models.signals import post_save
from django.dispatch import receiver

from workspaces.models import (
    Workspace,
    WorkspaceRole,
)
from workspaces import utils

@receiver(post_save, sender=Workspace)
def create_roleworkspace(sender, created, instance, **kwargs):
    if created: 
        user = utils.get_current_user_or_none()
        if user is not None:
            role = 'workspace_admin'
            WorkspaceRole.objects.create(
                user=user,
                workspace=instance,
                role=role
            )