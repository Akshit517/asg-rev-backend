from rest_framework import generics, permissions
from workspaces.models.workspace import Workspace
from .serializers import WorkspaceSerializer

class UserWorkspaceListView(generics.ListAPIView):
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Workspace.objects.filter(owner=user)

class CreateWorkspaceView(generics.CreateAPIView):
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
