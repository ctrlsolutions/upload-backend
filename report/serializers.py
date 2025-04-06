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
        # 1. Extract nested report data
        report_data = validated_data.pop('report')

        # 2. Get the user from the context (passed from the view)
        user = self.context['request'].user
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to create a report.")

        # 3. Create the base Report instance, assigning the user
        report_instance = Report.objects.create(**report_data, user_id=user)

        # 4. Create the ResearchReport instance, linking it to the base report
        research_report_instance = ResearchReport.objects.create(
            report=report_instance,
            **validated_data # Use remaining validated data for ResearchReport fields
        )
        return research_report_instance
    
    # OPTIONAL NI
    # def update(self, instance, validated_data):
    #     report_data = validated_data.pop('report', None)
    
    #     # Update base Report fields if report_data is provided
    #     if report_data:
    #         report_instance = instance.report
    #         for attr, value in report_data.items():
    #             setattr(report_instance, attr, value)
    #         report_instance.save()
    
    #     # Update ResearchReport fields
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    
    #     return instance


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
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to create a report.")

        report_instance = Report.objects.create(**report_data, user_id=user)

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
        if not user or not user.is_authenticated:
             raise serializers.ValidationError("User must be authenticated to create a report.")

        report_instance = Report.objects.create(**report_data, user_id=user)

        others_report_instance = OthersReport.objects.create(
            report=report_instance,
            **validated_data
        )
        return others_report_instance
