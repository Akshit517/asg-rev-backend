from rest_framework import serializers
from users.serializers import UserSerializer
from workspaces.models.assignment.assignment import (
    Assignment,
    Task,
)
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task','due_date']
        
class AssignmentSerializer(serializers.ModelSerializer):
    tasks =  TaskSerializer(many=True,required=False)
    class Meta:
        model = Assignment
        fields = ['description', 'for_teams', 'total_points', 'created_at', 'tasks']

    def create(self, validated_data):
        tasks_data = validated_data.pop('tasks', [])
        assignment = Assignment.objects.create(**validated_data)
        for task_data in tasks_data:
            Task.objects.create(assignment=assignment, **task_data)
        return assignment
    def update(self, instance, validated_data):
        tasks_data = validated_data.pop('tasks', None)
        instance.description = validated_data.get('description', instance.description)
        instance.for_teams = validated_data.get('for_teams', instance.for_teams)
        instance.total_points = validated_data.get('total_points', instance.total_points)
        instance.save()
        if tasks_data:
            instance.tasks.all().delete()
            for task_data in tasks_data:
                Task.objects.create(assignment=instance, **task_data)
        return instance
