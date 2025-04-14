from django.db import models
from django.contrib.postgres.fields import ArrayField
from user.models import CustomUser


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reports", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class PublicationType(models.TextChoices):
    PEER_REVIEWED_JOURNAL_ARTICLE = 'PEER_REVIEWED_JOURNAL_ARTICLE', 'Peer Reviewed Journal Article'
    BOOK = 'BOOK', 'Book'
    EDITED_OR_PEER_REVIEWED_BOOK_CHAPTER = 'EDITED_OR_PEER_REVIEWED_BOOK_CHAPTER', 'Edited or Peer Reviewed Book Chapter'
    PEER_REVIEWED_CONFERENCE_PAPER_PUBLICATION = 'PEER_REVIEWED_CONFERENCE_PAPER_PUBLICATION', 'Peer Reviewed Conference Paper Publication'
    OTHER = 'OTHER', 'Other'

class PublisherLocation(models.TextChoices):
    LOCAL = 'LOCAL', 'Local'
    INTERNATIONAL = 'INTERNATIONAL', 'International'

class PublisherType(models.TextChoices):
    COMMERCIAL = 'COMMERCIAL', 'Commercial'
    LEARNED_SOCIETY_AND_ASSOCIATION = 'LEARNED_SOCIETY_AND_ASSOCIATION', 'Learned Society and Association'
    UNIVERSITY_PRESS = 'UNIVERSITY_PRESS', 'University Press'
    
class ResearchReport(models.Model):
    report_id = models.OneToOneField(Report, on_delete=models.CASCADE, related_name="research_report")
    timeframe = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    name_of_researchers = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    source_of_funding = models.CharField(max_length=255)

class PublicationReport(models.Model):
    report_id = models.OneToOneField(Report, on_delete=models.CASCADE, related_name="publication_report")
    publication_title = models.CharField(max_length=255)
    publication_type = models.CharField(
        max_length=42,
        choices=PublicationType.choices
    )
    author_names = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    publication_date = models.DateField()
    publisher_name = models.CharField(max_length=255)
    publisher_type = models.CharField(
        max_length=32,
        choices=PublisherType.choices
    )
    publisher_location = models.CharField(
        max_length=20,
        choices=PublisherLocation.choices
    )
    editor_names = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    volume_number = models.CharField(max_length=255)
    issue_number = models.CharField(max_length=255)
    doi_or_url = models.URLField()
    isbn_or_issn = models.CharField(max_length=255)
    number_of_citations = models.IntegerField()

class PaperPresentationReport(models.Model): 
    report_id = models.OneToOneField(Report, on_delete=models.CASCADE, related_name="paper_presentation_report")
    research_title = models.CharField(max_length=255)
    presented_paper_title = models.CharField(max_length=255)
    presentation_type = models.CharField(max_length=100)
    conference_title = models.CharField(max_length=255)
    organizer_name = models.CharField(max_length=255)
    conference_location = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    conference_start_date = models.DateField()
    conference_end_date = models.DateField()
    presentation_date = models.DateField()

class PatentReport(models.Model):
    report_id = models.OneToOneField(Report, on_delete=models.CASCADE, related_name="patent_report") # Adjust related_name as needed
    patent_title = models.CharField(max_length=255)
    patent_type = models.CharField(max_length=100) 
    application_no = models.CharField(max_length=100) 
    # Using TextField for potentially long lists, consider ArrayField if DB supports and structure is needed
    inventors_name = models.TextField()
    owner_name = models.CharField(max_length=255)
    application_publication_date = models.DateField(null=True, blank=True) # Added null/blank
    patent_grant_date = models.DateField(null=True, blank=True) # Added null/blank
    registration_number = models.CharField(max_length=100, null=True, blank=True)
    commerical_product_name = models.CharField(max_length=255, null=True, blank=True) # Added null/blank
    industry_utilization = models.TextField(null=True, blank=True) # Changed to TextField, added null/blank

class OtherResearchReport(models.Model): 
    report_id = models.OneToOneField(Report, on_delete=models.CASCADE, related_name="other_research_report") # Adjust related_name as needed
    output_title = models.CharField(max_length=255)
    output_type = models.CharField(max_length=100) 
    public_event_type = models.CharField(max_length=100) 
    event_title = models.CharField(max_length=255)
    organizer_name = models.CharField(max_length=255)
    event_venue = models.CharField(max_length=255)
    event_location = models.CharField(max_length=255)
    event_start_date = models.DateField()
    event_end_date = models.DateField()
    output_firstshownorreleasedtopublic_date = models.DateField()
    industry_utilization = models.TextField(null=True, blank=True) # Changed to TextField, added null/blank

class TrainingReport(models.Model):
    report_id = models.OneToOneField(Report, on_delete=models.CASCADE, related_name="training_report") # Adjust related_name as needed
    activity_type = models.CharField(max_length=100) 
    course_or_service_title = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    schedule_special_notes = models.TextField(null=True, blank=True) # Changed to TextField, added null/blank
    # Using DecimalField for hours, adjust max_digits/decimal_places as needed
    hours_required_to_complete = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # Added null/blank
    number_of_trainees_served = models.PositiveIntegerField(null=True, blank=True) # Changed to PositiveIntegerField, added null/blank
    source_of_funding = models.CharField(max_length=255, null=True, blank=True) # Added null/blank

class ExtensionReport(models.Model): 
    report_id = models.OneToOneField(Report, on_delete=models.CASCADE, related_name="extension_report") # Adjust related_name as needed
    title = models.CharField(max_length=255)
    components = models.TextField() # Changed to TextField
    scope = models.CharField(max_length=100) 
    start_date = models.DateField()
    end_date = models.DateField()
    target_beneficiary_group = models.CharField(max_length=255)
    tbg_served = models.PositiveIntegerField(null=True, blank=True) # Changed to PositiveIntegerField, added null/blank
    source_of_funding = models.CharField(max_length=255, null=True, blank=True) # Added null/blank

class PartnershipReport(models.Model): 
    report_id = models.OneToOneField(Report, on_delete=models.CASCADE, related_name="partnership_report") # Adjust related_name as needed
    type_of_extension_activities_under_this_partnership = models.CharField(max_length=255)
    extension_partnership_title = models.CharField(max_length=255)
    up_scope_of_work = models.TextField() # Changed to TextField
    partner_stakeholder_name = models.CharField(max_length=255)
    stakeholder_category = models.CharField(max_length=100) 
    partnership_agreement_type = models.CharField(max_length=100) 
    partnership_agreement_effectivity_start_date = models.DateField()
    partnership_agreement_effectivity_end_date = models.DateField(null=True, blank=True) # Added null/blank

class OthersReport(models.Model):
    report_id = models.OneToOneField(Report, on_delete=models.CASCADE, related_name="others_report")
    description = models.TextField()