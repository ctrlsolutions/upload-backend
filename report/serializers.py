from rest_framework import serializers
from user.models import College, Department
from .models import Report, CustomUser

class ReportHistorySerializer(serializers.ModelSerializer):
    college = serializers.CharField(source='college_id.code', read_only=True)
    department = serializers.CharField(source='department_id.code', read_only=True)
    time_submitted = serializers.SerializerMethodField()
    report_type = serializers.CharField(source='get_report_type_display', read_only=True)
    formatted_author = serializers.SerializerMethodField()
    created_on = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ['created_on', 'time_submitted', 'formatted_author', 'college', 'department', 'report_type', 'title']
        
    def get_formatted_author(self, obj):
        first_name = obj.user_id.first_name or ""
        last_name = obj.user_id.last_name or ""
        full_name = f"{first_name} {last_name}".strip()

        name_parts = full_name.split()
        if len(name_parts) < 2:
            return full_name  # fallback for short names
        last_name = name_parts[-1]
        initials = ''.join([part[0] for part in name_parts[:-1]])
        return f"{last_name}, {initials.upper()}"

    def get_time_submitted(self, obj):
        return obj.created_on.strftime("%I:%M %p").lower()
    
    def get_created_on(self, obj):
        return obj.created_on.strftime("%B %d, %Y") 
