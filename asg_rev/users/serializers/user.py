from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
      
    def create(self, validated_data): 
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            auth_type=validated_data.get('auth_type', 'email'),
            profile_pic=validated_data.get(
                'profile_pic', 
                f'https://ui-avatars.com/api/?name={validated_data["username"]}'
                )
        )
        return user

    class Meta:
        model = User
        fields = ("id", "username", "password", "email", "profile_pic", "auth_type")