from rest_framework import serializers
from user.models import College  
from user.models import Department
from .models import Report, CustomUser

class ReportHistorySerializer(serializers.ModelSerializer):
    college = serializers.CharField(source='user_id.college.code', read_only=True)  # Access the college name
    department = serializers.CharField(source='user_id.department.code', read_only=True)  # Access the department name
    time_submitted = serializers.SerializerMethodField()
    report_type = serializers.SerializerMethodField()
    formatted_author = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ['created_on', 'time_submitted', 'formatted_author', 'college', 'department', 'report_type', 'title']

    def get_formatted_author(self, obj):
        full_name = obj.user_id.get_full_name() 
        name_parts = full_name.strip().split()
        
        if len(name_parts) < 2:
            return full_name  # fallback for short names

        last_name = name_parts[-1]
        initials = ''.join([part[0] for part in name_parts[:-1]])
        return f"{last_name}, {initials.upper()}"
    
    def get_time_submitted(self, obj):
        return obj.created_on.strftime("%I:%M %p").lower()

    def get_report_type(self, obj):
        if hasattr(obj, 'research_report'):
            return 'Research Report'
        elif hasattr(obj, 'publication_report'):
            return 'Publication Report'
        elif hasattr(obj, 'paper_report_model'):
            return 'Paper Presentation Report'
        elif hasattr(obj, 'patent_report_model'):
            return 'Patent Report'
        elif hasattr(obj, 'other_research_report_model'):
            return 'Other Research Output Report'
        elif hasattr(obj, 'training_report_model'):
            return 'Training Report'
        elif hasattr(obj, 'extension_report_model'):
            return 'Extension Report'
        elif hasattr(obj, 'partnership_report_model'):
            return 'Partnership Report'
        elif hasattr(obj, 'others_report'):
            return 'Others Report'
        return 'Unknown Report Type'
