from rest_framework.permissions import BasePermission

class IsWorkspaceOwnerOrAdmin(BasePermission): 
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if (obj.owner == request.user):
            return True

        return obj.workspace_role.filter(
            user=request.user, 
            role='workspace_admin'
            ).exists()

class IsWorkspaceOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.user.is_authenticated and obj.owner == request.user):
            return True
        return False

class IsWorkspaceMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return obj.workspace_role.filter(
            user=request.user,
            role='workspace_member'
        ).exists()            
