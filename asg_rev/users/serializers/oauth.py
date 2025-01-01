from rest_framework import serializers
class InputSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    redirect_uri = serializers.CharField(required=False)
    error = serializers.CharField(required=False)