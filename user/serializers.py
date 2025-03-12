from rest_framework import serializers
from .models import CustomUser

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
        email = data.get("email")
        password = data.get("password")

        # Authenticate user
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError({"error": "Invalid credentials."})

        # Save authenticated user for later use
        data["user"] = user
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'role']