import re

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers

from university.serializers import DepartmentSerializer, CollegeSerializer

from .models import CustomUser


UP_EMAIL_REGEX = re.compile(r'^[\w.+-]+@up\.edu\.ph$')
PASSWORD_REGEX = {
    'lowercase': re.compile(r'[a-z]'),
    'uppercase': re.compile(r'[A-Z]'),
    'digit': re.compile(r'\d'),
    'special': re.compile(r'[!@#$%^&*(),.?":{}|<>]'),
}

class SignUpSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only=True)
    password2 =serializers.CharField(write_only=True) 
    # access_token =serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2',  'first_name', 'middle_name', 'last_name', 'sex', 'birth_date', 'college', 'department', 'google_id']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'middle_name': {'required': False},
            'last_name': {'required': True},
            'sex': {'required': True},
            'birth_date': {'required': True},
            'college': {'required': True},
            'department': {'required': True},
            'google_id': {'required': False}
        }
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "Password does not match."})
        return data
    
    def validate_password(self, value):
        errors = []
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not PASSWORD_REGEX['lowercase'].search(value):
            errors.append("Password must contain at least one lowercase letter.")
        if not PASSWORD_REGEX['uppercase'].search(value):
            errors.append("Password must contain at least one uppercase letter.")
        if not PASSWORD_REGEX['digit'].search(value):
            errors.append("Password must contain at least one number.")
        if not PASSWORD_REGEX['special'].search(value):
            errors.append("Password must contain at least one special character.")

        try:
            validate_password(value)
        except DjangoValidationError as e:
            errors.extend(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return value
    
    def validate_email(self, value):
        if not UP_EMAIL_REGEX.match(value):
            raise serializers.ValidationError("Please use your UP email address.")
        return value
    
    
    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(**validated_data)

        user.set_password(validated_data["password"])
        user.save()

        return user

class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        return {
            "user": user,
        }
    
class UserProfileSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    college = CollegeSerializer(read_only=True)
    role = serializers.CharField(source='role.name')
    # profile_picture = serializers.ImageField(read_only=True)  # optional, if added later

    class Meta:
        model = CustomUser
        fields = [
            'user_id',
            'username',
            'first_name',
            'middle_name',
            'last_name',
            'sex',
            'email',
            'birth_date',
            'role',
            'college',
            'department',
        ]
