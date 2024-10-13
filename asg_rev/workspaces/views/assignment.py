from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from workspaces.models import Assignment, Channel
from workspaces.serializers import AssignmentSerializer
from workspaces.permissions import (
    IsWorkspaceMember,
    IsWorkspaceOwnerOrAdmin,
    IsChannelMember,
    IsReviewer, 
    IsReviewee,
)

class AssignmentView(RetrieveUpdateDestroyAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        channel_pk = self.kwargs.get('id')
        channel = get_object_or_404(Channel, id=channel_pk)
        return Assignment.objects.filter(id=channel)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsWorkspaceOwnerOrAdmin | (IsWorkspaceMember & IsReviewer)]
        else:
            permission_classes = [IsWorkspaceOwnerOrAdmin | (IsWorkspaceMember & IsChannelMember)]
        return [permission() for permission in permission_classes]

    #add reviewers
    #add reviewees
