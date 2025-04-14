from django.db import models
from user.models import CustomUser, Department, College

class Report(models.Model):
    class ReportType(models.TextChoices):
        RESEARCH = 'RESEARCH', 'Research Report'
        PUBLICATION = 'PUBLICATION', 'Publication Report'
        PAPER_PRESENTATION = 'PAPER_PRESENTATION', 'Paper Presentation Report'
        PATENT = 'PATENT', 'Patent Report'
        OTHER_RESEARCH = 'OTHER_RESEARCH', 'Other Research Output Report'
        TRAINING = 'TRAINING', 'Training Report'
        EXTENSION = 'EXTENSION', 'Extension Report'
        PARTNERSHIP = 'PARTNERSHIP', 'Partnership Report'
        OTHERS = 'OTHERS', 'Others Report'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reports")
    created_on = models.DateTimeField(auto_now_add=True)
    
    report_type = models.CharField(
        max_length=30,
        choices=ReportType.choices
    )


    department_id = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="reports"
    )

    college_id = models.ForeignKey(
        College,
        on_delete=models.PROTECT,
        related_name="reports"
    )

    def __str__(self):
        return self.title