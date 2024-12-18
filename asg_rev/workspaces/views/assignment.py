from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
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

class AssignmentView(RetrieveUpdateAPIView):
    serializer_class = AssignmentSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        channel_pk = self.kwargs.get('pk')
        channel = get_object_or_404(Channel, id=channel_pk)
        return Assignment.objects.filter(id=channel)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            permission_classes = [IsWorkspaceOwnerOrAdmin | (IsWorkspaceMember & IsReviewer)]
        else:
            permission_classes = [IsWorkspaceOwnerOrAdmin | (IsWorkspaceMember & IsChannelMember)]
        return [permission() for permission in permission_classes]

    def add_task(self, request):
        assignment = self.get_object()
        new_task =  request.data.get('task')

        if not new_task_data:
            return Response(
                {"detail": "Task data is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_tasks = list(assignment.tasks.values())
        existing_tasks.append(new_task_data)
        serializer = self.get_serializer(
            assignment, 
            data={"tasks": existing_tasks}, 
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return exceptions.ValidationError()
