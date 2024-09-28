from rest_framework import serializers
from users.models.user import User
from users.models.role import Role
from workspaces.models.channel import (
    Channel,
    ChannelRole,
)

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'category']        

class ChannelRoleSerializer(serializers.ModelSerializer):
    role_level = serializers.SerializerMethodField()

    class Meta:
        model = ChannelRole
        fields = ('id', 'user', 'channel', 'role', 'role_level')

    def get_role_level(self, obj):
        return 'channel'

    def validate_role(self, value):
        if value.role_level != 'channel':
            raise serializers.ValidationError("The role must be channel-level")
        return value
