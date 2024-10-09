from rest_framework import serializers
from users.models.user import User
from workspaces.models.category import (
    Category,
    CategoryRole,
)
from workspaces.models.channel import (
    Channel,
)
from workspaces.serializers.channel import (
    ChannelSerializer,
    ChannelRoleSerializer,
)

class CategorySerializer(serializers.ModelSerializer):
    channels = serializers.SerializerMethodField()
    workspace = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'workspace', 'channels']

    def get_channels(self, obj):
        channels = Channel.objects.filter(category=obj)
        return ChannelSerializer(channels, many=True, read_only=True).data

class CategoryRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryRole
        fields = ('id', 'user', 'category', 'role')
