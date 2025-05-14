from django.db import models
from django.contrib.postgres.fields import DateRangeField
from django.conf import settings

from user.models import College, Department

# TODO: make it work with users. perms and all that fuckery
# Choices for field types
TEXT = 'text'
NUMBER = 'number'
DATE = 'date'
SELECT = 'select'
MULTIPLE_CHOICE = 'multiple_choice'

TYPES = [
    (TEXT, 'Text'),
    (NUMBER, 'Number'),
    (DATE, 'Date'),
    (SELECT, 'Select'),
    (MULTIPLE_CHOICE, 'Multiple Choice'),
]

class Form(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Field(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=100)
    code = models.SlugField(max_length=50, blank=True, null=True, unique=False)
    type = models.CharField(max_length=20, choices=TYPES)

    # validation stuff
    required = models.BooleanField(default=True)
    regex_validation = models.CharField(max_length=100, blank=True, null=True)
    placeholder = models.CharField(max_length=100, blank=True, null=True)
    valid_date_range = DateRangeField(null=True, blank=True)

    # For multiple choice questions, store options
    options = models.JSONField(blank=True, null=True)  # Stores options for select or multiple choice fields
    
    def __str__(self):
        return self.label

class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    submitted_on = models.DateTimeField(auto_now_add=True)
    response = models.JSONField()  # Store responses as a JSON object, key:field_id, value:response

    def __str__(self):
        return f"Response for {self.form.title} by {self.user if self.user else 'Anonymous'}"

class ResponseDocument(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='supporting_documents')
    file = models.FileField(upload_to='form_documents/')
    
    def __str__(self):
        return f"Document for response {self.response.id} - Field: {self.field.label if self.field else 'General'}"

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports")
    created_on = models.DateTimeField(auto_now_add=True)

    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="reports"
    )

    college = models.ForeignKey(
        College, on_delete=models.PROTECT, related_name="reports"
    )

    form = models.ForeignKey(
        Form, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports' # not that required, but might be useful in the future for versioning
    )

    response = models.OneToOneField(
        Response, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports'
    )

    def __str__(self):
        return self.title
