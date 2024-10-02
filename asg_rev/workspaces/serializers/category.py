from rest_framework import serializers
from users.models.user import User
from workspaces.models.category import (
    Category,
    CategoryRole,
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','workspace']

class CategoryRoleSerializer(serializers.ModelSerializer):
    role_level = serializers.SerializerMethodField()

    class Meta:
        model = CategoryRole
        fields = ('id', 'user', 'category', 'role', 'role_level')

    def get_role_level(self, obj):
        return 'category'

    def validate_role(self, value):
        if value.role_level != 'category':
            raise serializers.ValidationError("The role must be category-level")
        return value

        
