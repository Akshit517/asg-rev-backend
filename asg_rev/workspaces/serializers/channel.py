from rest_framework import serializers
from users.models.user import User
from workspaces.models import (
    Workspace,
    Category,
    Channel,
    ChannelRole,
    Assignment,
    Task,
)
from workspaces.serializers.assignment import (
    AssignmentSerializer
)

class ChannelSerializer(serializers.ModelSerializer):
    assignment_data = AssignmentSerializer(write_only=True, required=False)
    assignment = AssignmentSerializer(read_only=True)

    class Meta:
        model = Channel
        fields = [
            'id',
            'name', 
            'assignment_data',
            'assignment'
        ]
        read_only_fields = [
            'category'
        ]
            
    def validate(self, data):
        category_id = self.context['view'].kwargs.get('category_pk')
        workspace_id = self.context['view'].kwargs.get('workspace_pk')
        try:
            workspace = Workspace.objects.get(id=workspace_id)
        except:
            raise serializers.ValidationError("workspace does not exist")
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError("Category does not exist.")
        data['category'] = category
        return data

    def create(self, validated_data):
        assignment_data = validated_data.pop('assignment_data', {})

        channel = Channel.objects.create(**validated_data)
        
        if assignment_data:
            assignment = Assignment.objects.create(
                id=channel,
                description=assignment_data.get('description', ''),
                total_points=assignment_data.get('total_points', 0),
                for_teams=assignment_data.get('for_teams', False)
            )
            tasks_data = assignment_data.pop('tasks',[])

            for task_data in tasks_data:
                Task.objects.create(assignment=assignment, **task_data)
        return channel

class ChannelRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelRole
        fields = ('id', 'user', 'channel', 'role')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ChannelRole.objects.all(),
                fields=['user', 'channel']
            )
        ]
