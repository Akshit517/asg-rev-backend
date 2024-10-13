from rest_framework import serializers 
from workspaces.models import (
    Submission,
    Iteration,
)
from workspaces.serializers.iteration import (
    IterationSerializer,
)

class SubmissionRevieweeSerializer(serializers.Serializer):
    class Meta:
        model = Submission
        fields = '__all__'

class SubmissionReviewerSerializer(serializers.ModelSerializer):
    iterations = IterationSerializer(
        many=True, 
        read_only=True,
        source='iteration_submissions'
    )

    class Meta:
        model = Submission
        fields = ['id', 'sender', 'assignment', 'created_at', 'iterations']

