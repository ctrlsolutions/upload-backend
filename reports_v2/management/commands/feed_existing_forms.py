from django.core.management.base import BaseCommand
from reports_v2.models import Form, Field
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

class Command(BaseCommand):
    help = 'Automate adding forms'

    def handle(self, *args, **kwargs):
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
            self.stdout.write(f"User '{username}' created.")
        else:
            self.stdout.write(f"A user with username '{username}' already exists. Skipping creation.")

        try:
            with transaction.atomic():
                form = Form.objects.create(title='Research', creator=user)

                form_1_Fields = [
                    Field(form=form, label='Research Project/Program/Work Title', type='text'),
                    Field(form=form, label='Number of Months in Original Timeframe', type='number'),
                    Field(form=form, label='Start Date', type='date'),
                    Field(form=form, label='End Date based on actual completion', type='date'),
                    Field(form=form, label='Name of Researcher/s', type='text'),
                    Field(
                        form=form,
                        label='Source of Majority Share of this Research Funding',
                        type='select',
                        options=[
                            'UP Entity',
                            'RP Government Entity or Public Sector Entity',
                            'RP Private Sector Entity',
                            'Foreign or Non-Domestic Entity'
                        ]
                    ),
                ]

                research_fields_response = Field.objects.bulk_create(form_1_Fields)
                if research_fields_response:
                    self.stdout.write("Research form fields successfully created.")

                pubform = Form.objects.create(title='Publication', creator=user)

                publication_Fields = [
                    Field(form=pubform, label='Publication Title', type='text', placeholder='title', required=True),
                    Field(form=pubform, label='Author/Co-Authors', type='text', placeholder='Name', required=True),
                    Field(form=pubform, label='Published or Accepted for Publication', type='date', required=True),
                    Field(form=pubform, label='Name of Journal/Book/Conference Publication/Other Publication', type='text', required=True),
                    Field(
                        form=pubform,
                        label='Type of Publication',
                        type='select',
                        required=True,
                        options=[
                            {'value': 'PEER_REVIEWED_JOURNAL_ARTICLE', 'label': 'Peer Reviewed Journal Article'},
                            {'value': 'BOOK', 'label': 'Book'},
                            {'value': 'EDITED_OR_PEER_REVIEWED_BOOK_CHAPTER', 'label': 'Edited or Peer Reviewed Book Chapter'},
                            {'value': 'PEER_REVIEWED_CONFERENCE_PAPER_PUBLICATION', 'label': 'Peer Reviewed Conference Paper Publication'},
                            {'value': 'OTHER', 'label': 'Other'},
                        ]
                    ),
                    Field(
                        form=pubform,
                        label='Type of Publisher',
                        type='select',
                        required=True,
                        options=[
                            {'value': 'COMMERCIAL', 'label': 'Commercial'},
                            {'value': 'LEARNED_SOCIETY_AND_ASSOCIATION', 'label': 'Learned Society and Association'},
                            {'value': 'UNIVERSITY_PRESS', 'label': 'University Press'},
                        ]
                    ),
                    Field(
                        form=pubform,
                        label='Location of Publisher',
                        type='select',
                        required=True,
                        options=[
                            {'value': 'LOCAL', 'label': 'Local'},
                            {'value': 'INTERNATIONAL', 'label': 'International'},
                        ]
                    ),
                    Field(form=pubform, label='Volume Number', type='text', required=True),
                    Field(form=pubform, label='Issue Number', type='text', required=True),
                    Field(form=pubform, label='Editor Names', type='text', required=True),
                    Field(form=pubform, label='DOI or URL', type='text', required=True),
                    Field(form=pubform, label='ISBN or ISSN', type='text', required=True),
                    Field(form=pubform, label='Number of Citations', type='number', required=True),
                ]

                publication_fields_response = Field.objects.bulk_create(publication_Fields)
                if publication_fields_response:
                    self.stdout.write("Publication form fields successfully created.")

        except Exception as e:
            self.stderr.write(f"Failed to create form or fields: {str(e)}")
