from django.core.management.base import BaseCommand
from reports_v2.models import Form, Field  # Import your models
from django.contrib.auth import get_user_model
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Automate adding forms'

    def handle(self, *args, **kwargs):

        from django.contrib.auth import get_user_model

        User = get_user_model()

        username = "testuser"
        email = "test@example.com"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email}
        )

        if created:
            user.set_password("password123")
            user.save()
            print(f"User '{username}' created.")
        else:
            print(f"A user with username '{username}' already exists. Skipping creation.")


        form_1_Fields = [
            Field(
                form=form,
                label='Research Project/Program/Work Title',
                type='text'
            ),
            Field(
                form=form,
                label='Number of Months in Original Timeframe',
                type='number'
            ),
            Field(
                form=form,
                label='Start Date',
                type='date'
            ),
            Field(
                form=form,
                label='End Date based on actual completion',
                type='date'
            ),
            Field(
                form=form,
                label='Name of Researcher/s',
                type='text'
            ),
            Field(
                form=form,
                label='Source of Majority Share of this Research Funding',
                type='select',
                # If using a JSONField or similar for options, adjust this accordingly
                options=[
                    'UP Entity',
                    'RP Government Entity or Public Sector Entity',
                    'RP Private Sector Entity',
                    'Foreign or Non-Domestic Entity'
                ]
            ),
        ]

        try:
            form = Form.objects.create(title='Research', creator=user)
            Field.objects.bulk_create(form_1_Fields)
            print("Form and fields created successfully.")

        except Exception as e:
            print("Failed to create form or fields:", str(e))
