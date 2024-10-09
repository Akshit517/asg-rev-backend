from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound
from workspaces.models import Workspace

class IsWorkspaceOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        print("executing admin permission workspace")
        workspace_id = view.kwargs.get('workspace_pk', view.kwargs.get('pk'))
        print(workspace_id)

        if not request.user.is_authenticated or not workspace_id:
            return False

        return request.user.workspace_role.filter(
            workspace_id=workspace_id,
            user=request.user,
            role='workspace_admin'
        ).exists()

class IsWorkspaceOwner(BasePermission):
    def has_permission(self, request, view):
        print("executing owner permission workspace")
        workspace_id = view.kwargs.get('workspace_pk', view.kwargs.get('pk'))
        print(workspace_id)

        if not request.user.is_authenticated or not workspace_id:
            return False

        try:
            workspace = Workspace.objects.get(id=workspace_id)
        except Workspace.DoesNotExist:
            raise NotFound("Workspace not found")

        return workspace.owner == request.user

class IsWorkspaceMember(BasePermission):
    def has_permission(self, request, view):
        print("executing member permission workspace")
        workspace_id = view.kwargs.get('workspace_pk', view.kwargs.get('pk'))
        print(workspace_id)
        if not request.user.is_authenticated or not workspace_id:
            return False

        return request.user.workspace_role.filter(
            workspace=workspace_id,
            user=request.user
        ).exists()
