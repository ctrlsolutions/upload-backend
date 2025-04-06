from django.db import models
from django.contrib.postgres.fields import ArrayField
from user.models import CustomUser

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

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reports")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
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
        max_length=20,
        choices=PublicationType.choices
    )
    author_names = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    publication_date = models.DateField()
    publisher_name = models.CharField(max_length=255)
    publisher_type = models.CharField(
        max_length=20,
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

class OthersReport(models.Model):
    report_id = models.OneToOneField(Report, on_delete=models.CASCADE, related_name="others_report")
    description = models.TextField()