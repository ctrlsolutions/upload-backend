from rest_framework import serializers
from .models import Form, Field, Response, ResponseDocument, Report
from user.models import CustomUser

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'label', 'type', 'required', 'regex_validation', 'placeholder', 'options','valid_date_range']

class FormSerializer(serializers.ModelSerializer):
    # Include the related fields for each form instance
    fields = FieldSerializer(many=True, read_only=True)
    class Meta:
        model = Form
        fields = ['id', 'name', 'code', 'description', 'active', 'fields']

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'form', 'user', 'submitted_on', 'response']

    def validate(self, data):
        # Add any additional validation logic if needed
        return data
    

class ResponseDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseDocument
        fields = '__all__'  # or maybe explicitly includes `field`

class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email']

class ReportSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer(read_only=True)
    form_name = serializers.CharField(source='form.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    college_name = serializers.CharField(source='college.name', read_only=True, allow_null=True)
    response_data = ResponseSerializer(source='response', read_only=True, allow_null=True) # Renamed to avoid conflict if you also want response ID

    class Meta:
        model = Report
        fields = [
            'id',
            'title',
            'user',                 # Output from BasicUserSerializer
            'created_on',           # From Report model
            'department',           # Foreign Key ID to Department
            'department_name',      # Sourced from Department.name
            'college',              # Foreign Key ID to College
            'college_name',         # Sourced from College.name
            'form',                 # Foreign Key ID to Form (can be null)
            'form_name',            # Sourced from Form.name (can be null if form is null)
            'response',             # Foreign Key ID to Response model (can be null)
            'response_data',        # Nested data from ResponseSerializer (can be null if response is null)
            # If you add a 'status' field to your Report model later, you can include 'status' here.
        ]
        read_only_fields = ['user', 'submission_date', 'created_at', 'updated_at']
        # Ensure the fields list matches your Report model.