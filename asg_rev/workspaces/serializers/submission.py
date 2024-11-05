from rest_framework import serializers 
from workspaces.models import (
    Submission,
    Iteration,
    Team,
    EarnedPoint
)
from workspaces.serializers.iteration import (
    IterationSerializer,
)
from users.serializers import (
    UserSerializer,
)

class SubmissionRevieweeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id','content','file']

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
    iterations = IterationSerializer(
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

class EarnedPointSerializer(serializers.ModelSerializer):
    reviewee = UserSerializer(required=False)
    reviewee_team = TeamSerializer(required=False)

    class Meta:
        model = EarnedPoint
        fields = ['assignment', 'reviewee', 'reviewee_team', 'earned_points']

    def validate(self, data):
        assignment = Assignment.objects.get(id=data['assignment'])
        
        if data.get('earned_points', 0) > assignment.total_points:
            raise serializers.ValidationError(
                f"Earnt points cannot exceed total points of {assignment.total_points}."
            )

        reviewee = data.get('reviewee')
        reviewee_team = data.get('reviewee_team')

        if assignment.for_teams:
            if reviewee is not None:
                raise serializers.ValidationError("reviewee cannot be set when for_teams is True.")
        else:
            if reviewee is None:
                raise serializers.ValidationError("either reviewee or reviewee_team must be provided.")

        if reviewee and reviewee_team:
            raise serializers.ValidationError("one of reviewee or reviewee_team must be set.")

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.reviewee_team:
            representation['reviewee_team'] = TeamSerializer(instance.reviewee_team).data
        return representation