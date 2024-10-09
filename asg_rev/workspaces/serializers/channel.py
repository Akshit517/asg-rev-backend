from rest_framework import serializers
from users.models.user import User
from workspaces.models.channel import (
    Channel,
    ChannelRole,
)
from workspaces.models.category import (
    Category,
)

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'category']
    
    def validate_workspace(self, value):
        category = self.initial_data.get('category')
        try:
            category = Category.objects.get(id=category)
        except Category.DoesNotExist:
            raise serializers.ValidationError("category does not exist.")

        if category.workspace != value:
            raise serializers.ValidationError("workspace does not match category workspace")

        return value

    def validate_category(self, value):
        category_id = self.initial_data.get('category')
        
        if not Category.objects.filter(id=category_id).exists():
            raise serializers.ValidationError("category does not exist.")
        
        return value 

class ChannelRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelRole
        fields = ('id', 'user', 'channel', 'role')

