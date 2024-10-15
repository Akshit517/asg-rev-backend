from rest_framework import status, permissions, exceptions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from users.models.user import User
from workspaces import utils
from workspaces.models.workspace import (
    Workspace, 
    WorkspaceRole,
)
from workspaces.models.category import (
    CategoryRole,
)
from workspaces.models.channel import (
    ChannelRole
)
from workspaces.serializers.workspace import (
    WorkspaceRoleSerializer, 
    WorkspaceSerializer
)
from workspaces.permissions.workspace import (
    IsWorkspaceMember, 
    IsWorkspaceOwnerOrAdmin
)

class WorkspaceViewSet(ModelViewSet):
    serializer_class = WorkspaceSerializer
    
    def get_queryset(self):
        user = self.request.user
        workspace_ids = WorkspaceRole.objects.filter(user=user).values_list('workspace', flat=True)
        return Workspace.objects.filter(id__in = workspace_ids)

    def perform_create(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ['list', 'create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsWorkspaceOwnerOrAdmin]
        elif self.action in ['retrieve']:
            self.permission_classes = [IsWorkspaceMember]

        return super().get_permissions()

class WorkspaceMemberView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST','DELETE']:
            permission_classes = [IsWorkspaceOwnerOrAdmin]
        else:  
            permission_classes = [IsWorkspaceMember]
        return [permission() for permission in permission_classes]

    def get(self, request, workspace_pk):
        queryset = WorkspaceRole.objects.filter(
            workspace_id=workspace_pk
        ).select_related('user')

        email = request.query_params.get('email')
        if email is not None:
            queryset = queryset.filter(user__email=email)
        
        serializer = WorkspaceRoleSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, workspace_pk):
        workspace = get_object_or_404(Workspace, pk=workspace_pk)
        
        user_email = request.data.get('user_email')
        role = request.data.get('role', 'workspace_member')  
        if not user_email:
            return exceptions.ValidationError("user email is required")

        user = get_object_or_404(User, email=user_email)
        workspace_role, created = WorkspaceRole.objects.update_or_create(
            user=user, 
            workspace=workspace,
            defaults={'role': role}
        )

        serializer = WorkspaceRoleSerializer(workspace_role)

        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    def delete(self, request, workspace_pk):
        email = request.data.get('user_email')
        if not email:
            return exceptions.ValidationError("user email is required")
        elif request.user.email == email:
            return exceptions.PermissionDenied("you can't remove yourself from workspace")

        user = get_object_or_404(User, email=email)
        workspace_role = get_object_or_404(WorkspaceRole, user=user, workspace_id=workspace_pk)
        workspace_role.delete()

        CategoryRole.objects.filter(
            user=user, 
            category__workspace_id=workspace_pk
        ).delete()

        ChannelRole.objects.filter(
            user=user, 
            channel__category__workspace_id=workspace_pk
        ).delete()

        return Response(
            {"detail": "Member has been removed from the all workspace related components"}, 
            status=status.HTTP_204_NO_CONTENT
        )
        
