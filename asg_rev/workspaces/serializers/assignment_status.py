from rest_framework import serializers
from workspaces.models.assignment.assignment_status import AssignmentStatus

class AssignmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentStatus
        fields = '__all__'

class AssignmentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentStatus
        fields = ['status', 'earned_points']
