from rest_framework import serializers
from .models import *

class SupportingDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportingDocument
        fields = ['file', 'owner']

class ReportSerializer(serializers.ModelSerializer):
    supporting_document = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Report
        fields = ['title', 'supporting_document']
        read_only_fields = ['id', 'user_id', 'created_on']

    def create(self, validated_data):
        print("Validated data at create():", validated_data)

        user = self.context['request'].user if 'request' in self.context else None
        if user and user.is_authenticated:
            validated_data['user_id'] = user
        else:
            print("WARNING: Anonymous user — 'user' not set on report.")

        supporting_document_data = validated_data.pop('supporting_document', [])
        
        report_instance = self.Meta.model.objects.create(**validated_data)

        for file in supporting_document_data:
            SupportingDocument.objects.create(file=file, owner=report_instance)

        return report_instance

class ResearchSerializer(ReportSerializer):
    class Meta(ReportSerializer.Meta):
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
        fields = ReportSerializer.Meta.fields + [
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

    
class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchReport
        fields =  ReportSerializer.Meta.fields + [
            'research_title',
            'presented_paper_title',
            'presentation_type',
            'conference_title',
            'organizer_name',
            'conference_location',
            'venue',
            'conference_start_date',
            'conference_end_date',
            'presentation_date'
        ]

    
class PatentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchReport
        fields =  ReportSerializer.Meta.fields + [
            'patent_title',
            'patent_type',
            'application_no',
            'inventors_name',
            'owner_name',
            'application_publication_date',
            'patent_grant_date',
            'registration_number',
            'commerical_product_name',
            'industry_utilization'
        ]

class OtherResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchReport
        fields =  ReportSerializer.Meta.fields + [
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
            'industry_utilization'
        ]
    
class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchReport
        fields =  ReportSerializer.Meta.fields + [
            'activity_type',
            'course_or_service_title',
            'venue',
            'start_date',
            'end_date',
            'schedule_special_notes',
            'hours_required_to_complete',
            'number_of_trainees_served',
            'source_of_funding'
        ]

class ExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchReport
        fields =  ReportSerializer.Meta.fields + [
            'title',
            'components',
            'scope',
            'start_date',
            'end_date',
            'target_beneficiary_group',
            'tbg_served',
            'source_of_funding'
        ]
    
class PartnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchReport
        fields =  ReportSerializer.Meta.fields + [
            'type_of_extension_activities_under_this_partnership',
            'extension_partnership_title',
            'up_scope_of_work',
            'partner_stakeholder_name',
            'stakeholder_category',
            'partnership_agreement_type',
            'partnership_agreement_effectivity_start_date',
            'partnership_agreement_effectivity_end_date'
        ]

class OthersSerializer(serializers.ModelSerializer):
    class Meta:
        model = OthersReport
        fields =  ReportSerializer.Meta.fields + ['report', 'description', 'file']

