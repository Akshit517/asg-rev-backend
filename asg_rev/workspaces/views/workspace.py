from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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
    permission_classes = [IsAuthenticated]
     
    def get_queryset(self):
        user = self.request.user
        print(user.id)
        workspace_ids = WorkspaceRole.objects.filter(user=user).values_list('workspace', flat=True)
        print(workspace_ids)
        print(Workspace.objects.filter(id__in = workspace_ids))
        return Workspace.objects.filter(id__in = workspace_ids)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsWorkspaceMember]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsWorkspaceOwnerOrAdmin]  

        return super().get_permissions()

    @action(detail=True,methods=['GET'])
    def get_category(self, request, pk=None):
        permission_classes = [IsWorkspaceMember]
        workspace = self.get_object()
        categories = Category.objects.filter(workspace=workspace)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)




