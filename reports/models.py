from django.db import models
from user.models import CustomUser

# Create your models here.
class Report(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reports")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class OthersReport(models.Model):
    report_id = models.OneToOneField(Report, on_delete=models.CASCADE, related_name="others_report")
    description = models.TextField()