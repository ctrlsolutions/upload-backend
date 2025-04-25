from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import DateRangeField
from django.conf import settings

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
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)  # To enable or disable form submission

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class Field(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=100)
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