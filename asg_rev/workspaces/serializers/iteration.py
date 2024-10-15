from rest_framework import serializers
from workspaces.models import Iteration

class IterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iteration
        fields = ['id', 'reviewee', 'reviewee_team', 'reviewer', 'submission', 'created_at']

    
