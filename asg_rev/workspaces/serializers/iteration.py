from rest_framework import serializers
from workspaces.models.assignment.iteration import (
    Iteration,
) 
from workspaces.models.assignment.assignment_status import (
    AssignmentStatus
)
from users.serializers import UserSerializer

class IterationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iteration
        fields = ['remarks']

class IterationReviewerSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    reviewee = UserSerializer(read_only=True)
    assignment_status = serializers.SerializerMethodField()

    class Meta:
        model = Iteration
        fields = ['id', 'reviewee', 'reviewer', 'submission', 'remarks', 'created_at', 'assignment_status']

    def get_assignment_status(self, obj):
        status = AssignmentStatus.objects.filter(
            assignment=obj.submission.assignment,
            reviewee=obj.submission.sender
        ).first()
        if status is None:
            status = AssignmentStatus.objects.create(
                assignment=obj.submission.assignment,
                reviewee=obj.submission.sender
            )
        if status:
            return {
                'status': status.status,
                'earned_points': status.earned_points
            }


class IterationRevieweeSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    assignment_status = serializers.SerializerMethodField()

    class Meta:
        model = Iteration
        fields = ['id', 'reviewer', 'remarks', 'created_at', 'assignment_status']

    def get_assignment_status(self, obj):
        status = AssignmentStatus.objects.filter(
            assignment=obj.submission.assignment,
            reviewee=obj.submission.sender
        ).first()
        if status is None:
            status = AssignmentStatus.objects.create(
                assignment=obj.submission.assignment,
                reviewee=obj.submission.sender
            )
        if status:
            return {
                'status': status.status,
                'earned_points': status.earned_points
            }
        return None
