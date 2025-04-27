from rest_framework import serializers
from .models import Form, Field, Response, ResponseDocument, ReportFormTemplate, Report
from django.contrib.auth import get_user_model


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'label', 'type', 'required', 'regex_validation', 'placeholder', 'options','valid_date_range']

class FormSerializer(serializers.ModelSerializer):
    # Include the related fields for each form instance
    fields = FieldSerializer(many=True, read_only=True)
    class Meta:
        model = Form
        fields = ['id', 'title', 'description', 'active', 'fields']
    

class ResponseDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseDocument
        fields = '__all__'  # or maybe explicitly includes `field`

class ReportFormTemplateSerializer(serializers.ModelSerializer):
    form = FormSerializer()

    class Meta:
        model = ReportFormTemplate
        fields = ['report_type', 'form']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'id', 
            'title', 
            'user', 
            'created_on', 
            'report_type', 
            'department', 
            'college', 
            'form', 
        ]
        # You can customize the fields if needed, for example, adding read_only fields
        read_only_fields = ['id', 'created_on']

    def validate_report_type(self, value):
        """ Custom validation for report_type if needed """
        if value not in dict(Report.ReportType.choices):
            raise serializers.ValidationError("Invalid report type.")
        return value

class ResponseSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='report.title')
    college = serializers.CharField(source='report.college.name')
    department = serializers.CharField(source='report.department.name')

    class Meta:
        model = Response
        fields = ['id', 'title', 'college', 'department', 'user', 'submitted_on', 'response']
