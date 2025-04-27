from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Form, Field, Response, ReportFormTemplate, Report
from django.db import transaction

User = get_user_model()

class FormSubmissionTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create Research form + fields + mapping
        with transaction.atomic():
            self.research_form = Form.objects.create(title='Research', creator=self.user)

            self.fields = Field.objects.bulk_create([
                Field(form=self.research_form, label='Research Project/Program/Work Title', type='text'),
                Field(form=self.research_form, label='Number of Months in Original Timeframe', type='number'),
                Field(form=self.research_form, label='Start Date', type='date'),
                Field(form=self.research_form, label='End Date based on actual completion', type='date'),
                Field(form=self.research_form, label='Name of Researcher/s', type='text'),
                Field(
                    form=self.research_form,
                    label='Source of Majority Share of this Research Funding',
                    type='select',
                    options=[
                        'UP Entity',
                        'RP Government Entity or Public Sector Entity',
                        'RP Private Sector Entity',
                        'Foreign or Non-Domestic Entity'
                    ]
                ),
            ])

            ReportFormTemplate.objects.create(
                report_type=Report.ReportType.RESEARCH,
                form=self.research_form
            )

    def test_submit_response_to_research_form(self):
        # Prepare a fake response dictionary (field.id ➔ fake value)
        response_data = {
            str(field.id): "Sample answer" if field.type == 'text' else 12 if field.type == 'number' else "2025-01-01"
            for field in self.fields
        }

        # Create a Response
        response = Response.objects.create(
            form=self.research_form,
            user=self.user,
            response=response_data
        )

        # Assertions
        self.assertEqual(response.form, self.research_form)
        self.assertEqual(response.user, self.user)
        self.assertEqual(len(response.response), len(self.fields))  # All fields answered
        for field in self.fields:
            self.assertIn(str(field.id), response.response)  # Check all fields are in response

        print("✅ Research form response successfully submitted and validated.")
