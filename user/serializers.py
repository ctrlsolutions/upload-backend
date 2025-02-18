from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'first_name', 'last_name', 'email', 'role', 'is_active']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']