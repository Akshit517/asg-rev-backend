from rest_framework import serializers
from users.models.user import User
from users.serializers import UserSerializer
from workspaces.models.workspace import (
    Workspace,
    WorkspaceRole,
)

class WorkspaceSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'icon', 'owner'] 
        read_only_fields = ['owner']

    def create(self, validated_data):
        request = self.context.get('request')
        workspace = Workspace.objects.create(
            owner=request.user,
            **validated_data
        )
        return workspace

class WorkspaceRoleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = WorkspaceRole
        fields = '__all__'
