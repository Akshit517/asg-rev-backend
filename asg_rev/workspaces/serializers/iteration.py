from rest_framework import serializers
from workspaces.models import Iteration

class IterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iteration
        fields = ['id', 'reviewee', 'reviewee_team', 'reviewer', 'submission', 'created_at']

    def validate_reviewer(self, value):
        assignment = self.context['assignment']
        if not assignment.channel.channelrole_set.filter(
            user=value, 
            role='reviewer'
        ).exists():
            raise serializers.ValidationError(f"{value.username} is not assigned as a reviewer for this assignment.")
        return value
