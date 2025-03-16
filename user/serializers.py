from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class SignUpSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only=True)
    password2 =serializers.CharField(write_only=True) 

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2',  'first_name', 'middle_name', 'last_name', 'sex', 'birthdate']
    
    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop("password2")

        user = CustomUser(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user
    
class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return {"user": user}

    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'role']