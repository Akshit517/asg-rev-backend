from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound
from workspaces.models import Workspace

class WorkspacePermissionMixin:
    def get_workspace(self, view):
        workspace_id = view.kwargs.get('workspace_pk', view.kwargs.get('pk'))
        if not workspace_id:
            return None
        try:
            return Workspace.objects.get(id=workspace_id)
        except Workspace.DoesNotExist:
            raise NotFound("Workspace not found")

    def has_role_permission(self, request, view, role_pattern):
        if not request.user.is_authenticated:
            return False

        workspace = self.get_workspace(view)
        if not workspace:
            return False

        return request.user.workspace_role.filter(
            user=request.user,
            workspace=workspace, 
            role__startswith=role_pattern
        ).exists()

    def is_workspace_owner(self, request, view):
        if not request.user.is_authenticated:
            return False

        workspace = self.get_workspace(view)
        if not workspace:
            return False

        return (workspace.owner == request.user)


class IsWorkspaceOwnerOrAdmin(WorkspacePermissionMixin, BasePermission):
    def has_permission(self, request, view):
        print("Executing admin permission workspace")
        return self.has_role_permission(request, view, 'workspace_admin')

class IsWorkspaceOwner(WorkspacePermissionMixin, BasePermission):
    def has_permission(self, request, view):
        print("Executing owner permission workspace")
        return self.is_workspace_owner(request, view)

class IsWorkspaceMember(WorkspacePermissionMixin, BasePermission):
    def has_permission(self, request, view):
        print("Executing member permission workspace")
        return self.has_role_permission(request, view, 'workspace_')
