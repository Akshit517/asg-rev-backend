from rest_framework import serializers 
from workspaces.models import (
    Submission,
    Iteration,
    Team
)
from workspaces.serializers.iteration import (
    IterationRevieweeSerializer,
)
from users.serializers import (
    UserSerializer,
)

class SubmissionRevieweeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id','content','file','submitted_at']

    def create(self, validated_data):
        sender = validated_data.pop('sender')  
        assignment = validated_data.pop('assignment')

        submission = Submission.objects.create(
           sender=sender,
           assignment=assignment,
            **validated_data
        )

        return submission

class SubmissionReviewerSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    iterations = IterationRevieweeSerializer(
        many=True, 
        read_only=True,
        source='iteration_submissions'
    )

    class Meta:
        model = Submission
        fields = ['id', 'sender', 'assignment', 'submitted_at', 'iterations']

class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = ['id','assignment,''team_name','team_leader','members']

    def validate_assignment(self , value):
        if not value.for_teams:
            raise serializers.ValidationError(
                "This assignment does not allow team submissions"
            )
        return value
