
from rest_framework import serializers
from .models import User


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ('email', 'name', 'avatar', 'password1', 'password2')
        
    def create(self, validated_data):
        # Remove password2 since we don't need to save it
        validated_data.pop('password2')

        # Create the user with the provided password
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            avatar=validated_data.get('avatar')
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user