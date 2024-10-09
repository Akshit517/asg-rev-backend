from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from users.models.user import ( 
    User,
)
from workspaces.models.workspace import (
    Workspace,
    WorkspaceRole
)
from workspaces.models.category import (
    Category,
)
from workspaces.serializers.workspace import (
    WorkspaceSerializer,
    WorkspaceRoleSerializer
)
from workspaces.serializers.category import (
    CategorySerializer,
)
from workspaces.permissions.workspace import (
    IsWorkspaceMember,
    IsWorkspaceOwner, 
    IsWorkspaceOwnerOrAdmin,
)
from rest_framework.permissions import (
    IsAuthenticated,
)

class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer
    
    def get_queryset(self):
        user = self.request.user
        workspace_ids = WorkspaceRole.objects.filter(user=user).values_list('workspace', flat=True)
        return Workspace.objects.filter(id__in = workspace_ids)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsWorkspaceOwnerOrAdmin]
        elif self.action in ['retrieve']:
            self.permission_classes = [IsWorkspaceMember]

        return super().get_permissions()

    @action(detail=True, methods=['POST'], permission_classes=[IsWorkspaceOwnerOrAdmin])
    def add_member(self, request, pk=None):
        workspace = self.get_object()  
        user_id = request.data.get('user_id')
        role = request.data.get('role','workspace_member')

        if not user_id or not role:
            raise ValidationError({"detail": "Both 'user_id' and 'role' fields are required."})
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                    {"detail": "User not found."}, 
                    status=status.HTTP_404_NOT_FOUND
                )

        if WorkspaceRole.objects.filter(user=user, workspace=workspace).exists():
            return Response(
                    {"detail": "User is already a member of the workspace."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        workspace_role = WorkspaceRole.objects.create(user=user, workspace=workspace, role=role)
        serializer = WorkspaceRoleSerializer(workspace_role)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)