from rest_framework import serializers
from .models import Report, ResearchReport, PublicationReport, OthersReport

class SubmitReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'title', 'user_id', 'created_on']
        read_only_fields = ['id', 'user_id', 'created_on']


class ResearchSerializer(serializers.ModelSerializer):
    report = SubmitReportSerializer()

    class Meta:
        model = ResearchReport
        fields = [
            'report',
            'id',
            'timeframe',
            'start_date',
            'end_date',
            'name_of_researchers',
            'source_of_funding'
        ]

    def create(self, validated_data):
        report_data = validated_data.pop('report')

        user = self.context['request'].user
        report_instance = None
        if not user or not user.is_authenticated:
            # raise serializers.ValidationError("User must be authenticated to create a report.")
            report_instance = Report.objects.create(**report_data, user_id=user)
        else:
            print("WARNING: Creating report with user_id=NULL during AllowAny testing.")
            report_instance = Report.objects.create(**report_data)

        research_report_instance = ResearchReport.objects.create(
            report=report_instance,
            **validated_data 
        )
        return research_report_instance

class PublicationSerializer(serializers.ModelSerializer):
    report = SubmitReportSerializer(read_only=True)

    class Meta:
        model = PublicationReport
        fields = [
            'report',
            'id',
            'publication_title',
            'publication_type',
            'author_names',
            'publication_date',
            'publisher_name',
            'publisher_type',
            'publisher_location',
            'editor_names',
            'volume_number',
            'issue_number',
            'doi_or_url',
            'isbn_or_issn',
            'number_of_citations'
        ]

    def create(self, validated_data):
        report_data = validated_data.pop('report')

        user = self.context['request'].user
        report_instance = None
        if not user or not user.is_authenticated:
            # raise serializers.ValidationError("User must be authenticated to create a report.")
            report_instance = Report.objects.create(**report_data, user_id=user)
        else:
            print("WARNING: Creating report with user_id=NULL during AllowAny testing.")
            report_instance = Report.objects.create(**report_data)

        publication_report_instance = PublicationReport.objects.create(
            report=report_instance,
            **validated_data
        )
        return publication_report_instance

class OthersSerializer(serializers.ModelSerializer):
    report = SubmitReportSerializer(read_only=True)

    class Meta:
        model = OthersReport
        fields = ['report', 'description']

    def create(self, validated_data):
        report_data = validated_data.pop('report')

        user = self.context['request'].user
        report_instance = None
        if not user or not user.is_authenticated:
            # raise serializers.ValidationError("User must be authenticated to create a report.")
            report_instance = Report.objects.create(**report_data, user_id=user)
        else:
            print("WARNING: Creating report with user_id=NULL during AllowAny testing.")
            report_instance = Report.objects.create(**report_data)

        others_report_instance = OthersReport.objects.create(
            report=report_instance,
            **validated_data
        )
        return others_report_instance
