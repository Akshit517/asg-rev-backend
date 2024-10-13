from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from workspaces.models import (
    Category,
    Channel, 
    ChannelRole,
    Assignment,
)
from workspaces.serializers import (
    ChannelSerializer, 
    AssignmentSerializer
)
from workspaces.permissions import (
    IsReviewer, 
    IsReviewee, 
    IsChannelMember,
    IsWorkspaceOwnerOrAdmin,
    IsWorkspaceMember,
)

class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer

    def get_queryset(self):
        user = self.request.user
        category_id = self.kwargs.get('category_pk')
        channel_ids = ChannelRole.objects.filter(user=user).values_list('channel', flat=True)
        return Channel.objects.filter(
            id__in=channel_ids,
            category_id=category_id
        )

    def perform_create(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [IsWorkspaceOwnerOrAdmin | IsReviewer]
        elif self.action in ['list']:
            permission_classes = [ (IsWorkspaceOwnerOrAdmin | IsWorkspaceMember) ]
        elif  self.action in ['retrieve']:
            permission_classes = [(IsWorkspaceOwnerOrAdmin | IsWorkspaceMember) & IsChannelMember ]

        return [permission() for permission in permission_classes]
