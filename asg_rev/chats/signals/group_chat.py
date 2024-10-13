from django.db.models.signals import post_save
from django.dispatch import receiver
from workspaces.models import (
    ChannelRole,
)
from assignment.models import (
    GroupChat,
)

@receiver(post_save, sender=ChannelRole)
def add_to_groupchat(sender, instance, created, **kwargs):
    if created:
        try:
            group_chat = GroupChat.objects.get(channel=instance.channel)
            group_chat.members.add(instance.user)
        except GroupChat.DoesNotExist:
            group_chat = GroupChat.objects.create(channel=instance.channel)
            group_chat.members.add(instance.user)
