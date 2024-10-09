from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from workspaces.models import (
    Category,
    Channel,
)
from workspaces.serializers import ChannelSerializer
from workspaces.permissions import (
    IsReviewer, 
    IsReviewee,
)

class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer

    def get_queryset(self):
        user = self.request.user
        category_id = self.kwargs.get('category_pk')
        
        if not user.channel_role.filter(channel__category_id=category_id).exists():
            return Channel.objects.none()

        return Channel.objects.filter(category_id=category_id)

    def perform_create(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [IsReviewer]
        elif self.action in ['list','retrieve']:
            permission_classes = [IsReviewee]

        return [permission() for permission in permission_classes]
