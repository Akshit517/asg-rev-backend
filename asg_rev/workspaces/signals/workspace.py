from django.db.models.signals import post_save
from django.dispatch import receiver
from workspaces.models.workspace import Workspace

@receiver(post_save,sender=Workspace)
def create_roleworkspace(sender, created, instance, **kwargs):
    if created:
        instance.user = sender.owner
        instance.workspace = sender
        instance.role = 'workspace_admin'
        instance.save()
    return instance