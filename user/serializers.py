from rest_framework import serializers
from .models import CustomUser, Department, College
from django.contrib.auth import authenticate


class SignUpSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only=True)
    password2 =serializers.CharField(write_only=True) 

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2',  'first_name', 'middle_name', 'last_name', 'sex', 'birth_date', 'college', 'department']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop("password2")

        user = CustomUser.objects.create_user(**validated_data)

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
        
        return {
            "user": user,
        }
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_id', 'name']

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['college_id', 'name']
    
class UserProfileSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    college = CollegeSerializer(read_only=True)
    role = serializers.CharField(source='role.name')

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'role',
            'college',
            'department',
        ]


class CollegeDepartmentsSerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True)

    class Meta:
        model = College
        fields = ['college_id', 'name', 'departments']
