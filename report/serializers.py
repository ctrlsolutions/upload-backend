from rest_framework import serializers
from .models import Report, ResearchReport, PublicationReport, OthersReport

class SubmitReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'title', 'user_id', 'created_on']
        read_only_fields = ['id', 'user_id', 'created_on']


class ResearchSerializer(serializers.ModelSerializer):
    report = SubmitReportSerializer(required=False)

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
        report_data = validated_data.pop('report', None)
        user = self.context['request'].user if 'request' in self.context else None
        report_instance = None

        if report_data:
            if user and user.is_authenticated:
                report_instance = Report.objects.create(**report_data, user_id=user)
            else:
                print("WARNING: Creating report without user during unauthenticated request.")
                report_instance = Report.objects.create(**report_data)
        else:
            default_report_data = {'title': 'Untitled Research'} # Add default title or other fields
            if user and user.is_authenticated:
                report_instance = Report.objects.create(**default_report_data, user_id=user)
            else:
                report_instance = Report.objects.create(**default_report_data)

        research_report_instance = ResearchReport.objects.create(
            report_id=report_instance,  # Assign the Report instance directly
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
        user = self.context['request'].user if 'request' in self.context else None
        report_instance = None

        if user and user.is_authenticated:
            report_instance = Report.objects.create(**report_data, user_id=user)
        else:
            print("WARNING: Creating report without user during unauthenticated request.")
            report_instance = Report.objects.create(**report_data)

        publication_report_instance = PublicationReport.objects.create(
            report_id=report_instance,
            **validated_data
        )
        return publication_report_instance
    
class PaperSerializer(serializers.ModelSerializer):
    report = SubmitReportSerializer(read_only=True)

    class Meta:
        model = ResearchReport
        fields = [
            'report',
            'id',
            'research_title',
            'presented_paper_title',
            'presentation_type',
            'conference_title',
            'organizer_name',
            'conference_location',
            'venue',
            'conference_start_date',
            'conference_end_date',
            'presentation_date',
        ]

    def create(self, validated_data):
        report_data = validated_data.pop('report')
        user = self.context['request'].user if 'request' in self.context else None
        report_instance = None

        if user and user.is_authenticated:
            report_instance = Report.objects.create(**report_data, user_id=user)
        else:
            print("WARNING: Creating report without user during unauthenticated request.")
            report_instance = Report.objects.create(**report_data)

        paper_report_instance = ResearchReport.objects.create(
            report_id=report_instance,
            **validated_data
        )
        return paper_report_instance
    
class PatentSerializer(serializers.ModelSerializer):
    report = SubmitReportSerializer(read_only=True)

    class Meta:
        model = ResearchReport
        fields = [
            'report',
            'id',
            'patent_title',
            'patent_type',
            'application_no',
            'inventors_name',
            'owner_name',
            'application_publication_date',
            'patent_grant_date',
            'registration_number',
            'commerical_product_name',
            'industry_utilization',
        ]

    def create(self, validated_data):
        report_data = validated_data.pop('report')
        user = self.context['request'].user if 'request' in self.context else None
        report_instance = None

        if user and user.is_authenticated:
            report_instance = Report.objects.create(**report_data, user_id=user)
        else:
            print("WARNING: Creating report without user during unauthenticated request.")
            report_instance = Report.objects.create(**report_data)

        patent_report_instance = ResearchReport.objects.create(
            report_id=report_instance,
            **validated_data
        )
        return patent_report_instance
    
class OtherResearchSerializer(serializers.ModelSerializer):
    report = SubmitReportSerializer(read_only=True)

    class Meta:
        model = ResearchReport
        fields = [
            'report',
            'id',
            'output_title',
            'output_type',
            'public_event_type',
            'event_title',
            'organizer_name',
            'event_venue',
            'event_location',
            'event_start_date',
            'event_end_date',
            'output_firstshownorreleasedtopublic_date',
            'industry_utilization',
        ]

    def create(self, validated_data):
        report_data = validated_data.pop('report')
        user = self.context['request'].user if 'request' in self.context else None
        report_instance = None

        if user and user.is_authenticated:
            report_instance = Report.objects.create(**report_data, user_id=user)
        else:
            print("WARNING: Creating report without user during unauthenticated request.")
            report_instance = Report.objects.create(**report_data)

        other_research_report_instance = ResearchReport.objects.create(
            report_id=report_instance,
            **validated_data
        )
        return other_research_report_instance
    
class TrainingSerializer(serializers.ModelSerializer):
    report = SubmitReportSerializer(read_only=True)

    class Meta:
        model = ResearchReport
        fields = [
            'report',
            'id',
            'activity_type',
            'course_or_service_title',
            'venue',
            'start_date',
            'end_date',
            'schedule_special_notes',
            'hours_required_to_complete',
            'number_of_trainees_served',
            'source_of_funding',
        ]

    def create(self, validated_data):
        report_data = validated_data.pop('report')
        user = self.context['request'].user if 'request' in self.context else None
        report_instance = None

        if user and user.is_authenticated:
            report_instance = Report.objects.create(**report_data, user_id=user)
        else:
            print("WARNING: Creating report without user during unauthenticated request.")
            report_instance = Report.objects.create(**report_data)

        training_report_instance = ResearchReport.objects.create(
            report_id=report_instance,
            **validated_data
        )
        return training_report_instance
    
class ExtensionSerializer(serializers.ModelSerializer):
    report = SubmitReportSerializer(read_only=True)

    class Meta:
        model = ResearchReport
        fields = [
            'report',
            'id',
            'title',
            'components',
            'scope',
            'start_date',
            'end_date',
            'target_beneficiary_group',
            'tbg_served',
            'source_of_funding',
        ]

    def create(self, validated_data):
        report_data = validated_data.pop('report')
        user = self.context['request'].user if 'request' in self.context else None
        report_instance = None

        if user and user.is_authenticated:
            report_instance = Report.objects.create(**report_data, user_id=user)
        else:
            print("WARNING: Creating report without user during unauthenticated request.")
            report_instance = Report.objects.create(**report_data)

        extension_report_instance = ResearchReport.objects.create(
            report_id=report_instance,
            **validated_data
        )
        return extension_report_instance
    
class PartnershipSerializer(serializers.ModelSerializer):
    report = SubmitReportSerializer(read_only=True)

    class Meta:
        model = ResearchReport
        fields = [
            'report',
            'id',
            'type_of_extension_activities_under_this_partnership',
            'extension_partnership_title',
            'up_scope_of_work',
            'partner_stakeholder_name',
            'stakeholder_category',
            'partnership_agreement_type',
            'partnership_agreement_effectivity_start_date',
            'partnership_agreement_effectivity_end_date',
        ]

    def create(self, validated_data):
        report_data = validated_data.pop('report')
        user = self.context['request'].user if 'request' in self.context else None
        report_instance = None

        if user and user.is_authenticated:
            report_instance = Report.objects.create(**report_data, user_id=user)
        else:
            print("WARNING: Creating report without user during unauthenticated request.")
            report_instance = Report.objects.create(**report_data)

        partnership_report_instance = ResearchReport.objects.create(
            report_id=report_instance,
            **validated_data
        )
        return partnership_report_instance

class OthersSerializer(serializers.ModelSerializer):
    report = SubmitReportSerializer(read_only=True)

    class Meta:
        model = OthersReport
        fields = ['report', 'description']

    def create(self, validated_data):
        report_data = validated_data.pop('report')
        user = self.context['request'].user if 'request' in self.context else None
        report_instance = None

        if user and user.is_authenticated:
            report_instance = Report.objects.create(**report_data, user_id=user)
        else:
            print("WARNING: Creating report without user during unauthenticated request.")
            report_instance = Report.objects.create(**report_data)

        others_report_instance = OthersReport.objects.create(
            report_id=report_instance,
            **validated_data
        )
        return others_report_instance
