from django.db.models.signals import post_save
from django.dispatch import receiver

from workspaces.models.workspace import (
    Workspace,
    WorkspaceRole,
)
from users.models.user import User

from crum import get_current_user

def get_current_user_or_none():
    u = get_current_user()
    if not isinstance(u, User):
        return None
    return u

@receiver(post_save, sender=Workspace)
def create_roleworkspace(sender, created, instance, **kwargs):
    if created: 
        user = get_current_user_or_none()
        if user is not None:
            role = 'workspace_admin'
            WorkspaceRole.objects.create(
                user=user,
                workspace=instance,
                role=role
            )