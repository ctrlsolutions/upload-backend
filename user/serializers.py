from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password1 =serializers.CharField(write_only=True)
    password2 =serializers.CharField(write_only=True) 

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2',  'first_name', 'middle_name', 'last_name', 'sex', 'birthdate']
    
    def validate(self, data):
        # Check if passwords match
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            middle_name=validated_data.get('middle_name', ''),
            last_name=validated_data['last_name'],
            sex=validated_data['sex'],
            birthdate=validated_data['birthdate']
        )
        user.set_password(validated_data['password1'])
        user.set_password(validated_data['password2'])
        user.save()
        return user