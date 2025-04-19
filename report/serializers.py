from rest_framework import serializers
from .models import *


class SupportingDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportingDocument
        fields = ['file']
        read_only_fields = ['owner']


class ReportSerializer(serializers.ModelSerializer):
    supporting_document = SupportingDocumentSerializer(many=True, required=False)
    class Meta:
        model = Report
        fields = ['title', 'created_on', 'supporting_document']
        read_only_fields = ['id', 'user_id', 'created_on']

    def create(self, validated_data):
        user = self.context['request'].user if 'request' in self.context else None
        validated_data['user'] = user
        if not user or not user.is_authenticated: #for dev
            print("WARNING: Creating report without user during unauthenticated request.")

        supporting_document_data = validated_data.pop('supporting_document',[])
        report_instance = Report.objects.create(**validated_data)

        if supporting_document_data:
            serialized_document = SupportingDocumentSerializer(
                data=supporting_document_data,
                many=True,
                context=self.context
            )
            serialized_document.is_valid(raise_exception=True)
            serialized_document.save(owner=report_instance)


        return report_instance

class ResearchSerializer(ReportSerializer):
    class Meta:
        model = ResearchReport
        fields = ReportSerializer.Meta.fields + [
            'timeframe',
            'start_date',
            'end_date',
            'name_of_researchers',
            'source_of_funding'
        ]


class PublicationSerializer(serializers.ModelSerializer):

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
            'number_of_citations',
            'file'
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
            'file'
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
            'file'
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
            'file'
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
            'file'
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
            'file'
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
            'file'
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

    class Meta:
        model = OthersReport
        fields = ['report', 'description', 'file']

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
