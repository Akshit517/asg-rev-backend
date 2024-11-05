from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    
    def validate(self, data):
        data['profile_pic'] = data.get('profile_pic', f'https://ui-avatars.com/api/?name={data["username"]}')
        
        return data
        
    class Meta:
        model = User
        fields = ("id", "username", "password", "email", "profile_pic", "auth_type")