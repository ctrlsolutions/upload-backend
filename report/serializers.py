from rest_framework import serializers
from .models import Form, Field, Response, ResponseDocument, ReportFormTemplate

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

class ReportFormTemplateSerializer(serializers.ModelSerializer):
    form = FormSerializer()

    class Meta:
        model = ReportFormTemplate
        fields = ['report_type', 'form']
