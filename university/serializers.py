from rest_framework import serializers

from .models import Department, College

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_id', 'name']

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['college_id', 'name', 'code']

class CollegeDepartmentsSerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True)

    class Meta:
        model = College
        fields = ['college_id', 'name', 'departments']
