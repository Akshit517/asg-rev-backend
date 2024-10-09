from rest_framework import serializers
from users.models.user import User
from workspaces.models.workspace import (
    Workspace,
    WorkspaceRole,
)

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'

class WorkspaceRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceRole
        fields = '__all__'

