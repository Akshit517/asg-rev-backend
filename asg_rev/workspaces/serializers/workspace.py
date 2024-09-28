from rest_framework import serializers
from users.models.user import User
from users.models.role import Role
from workspaces.models.workspace import (
    Workspace,
    WorkspaceRole,
)

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ('id', 'name', 'icon')  
        read_only_fields = ('owner',) 

class WorkspaceRoleSerializer(serializers.ModelSerializer):
    role_level = serializers.SerializerMethodField()

    class Meta:
        model = WorkspaceRole
        fields = ('id', 'user', 'workspace', 'role', 'role_level')

    def get_role_level(self, obj):
        return 'workspace'

    def validate_role(self, value):
        if value.role_level != 'workspace':
            raise serializers.ValidationError("The role must be a workspace-level role.")
        return value
