from django.db.models.signals import post_save
from django.dispatch import receiver
from workspaces.models.channel import Channel
from workspaces.models import ChannelRole

@receiver(post_save, sender=Channel)
def create_default_channel_roles(sender, instance, created, **kwargs):
    if created:      
        workspace_owner = instance.category.workspace.owner  
        ChannelRole.objects.create(user=workspace_owner, channel=instance, role='reviewer')
