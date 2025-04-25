from django.core.management.base import BaseCommand
from reports_v2.models import Form, Field
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

# TODO: finish default
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

                paperform = Form.objects.create(title='Research paper', creator=user)
                paper_presentation_Fields = [
                    Field(
                        form=paperform,
                        label='Research Project/Program/Work Title',
                        type='select',
                        placeholder='Select Research Title',
                        required=True,
                        options=[
                            {'value': 'Project ISAAC: Isolation, Screening, and Antimicrobial Activity of Compounds from Actinobacteria in Mainit Hot Springs, Cebu, Philippines', 'label': 'Project ISAAC: Isolation, Screening, and Antimicrobial Activity of Compounds from Actinobacteria in Mainit Hot Springs, Cebu, Philippines'},
                            {'value': 'An Edge-Based Model of SEIR Epidemics on Static Random Networks', 'label': 'An Edge-Based Model of SEIR Epidemics on Static Random Networks'},
                            {'value': 'On dual B-filters and Dual B-subalgebras in a Topolological Dual B-algebra', 'label': 'On dual B-filters and Dual B-subalgebras in a Topolological Dual B-algebra'},
                            {'value': 'Survey of Heatwaves in the Philippine Seas', 'label': 'Survey of Heatwaves in the Philippine Seas'},
                            {'value': 'Relationship between pearl formation and associated biofouling organisms in the pearl oysters of the Arabian Gulf', 'label': 'Relationship between pearl formation and associated biofouling organisms in the pearl oysters of the Arabian Gulf'},
                            {'value': 'Impacts of heatwaves and toxic algal blooms on the physiological performance and future aquaculture of the oysters Ostrea edulis and Magallana (Crassostrea) gigas', 'label': 'Impacts of heatwaves and toxic algal blooms on the physiological performance and future aquaculture of the oysters Ostrea edulis and Magallana (Crassostrea) gigas'},
                            {'value': 'River Ecosystem Health Assessment using Biomonitoring Tools', 'label': 'River Ecosystem Health Assessment using Biomonitoring Tools'},
                            {'value': 'Other', 'label': 'Other'},
                        ]
                    ),
                    Field(form=paperform, label='Title of Paper Presented', type='text', placeholder='Title of Paper Presented', required=True),
                    Field(
                        form=paperform,
                        label='Type of Presentation',
                        type='select',
                        required=True,
                        options=[
                            {'value': 'Oral Presentation', 'label': 'Oral Presentation'},
                            {'value': 'Poster Presentation', 'label': 'Poster Presentation'},
                        ]
                    ),
                    Field(form=paperform, label='Title of Conference', type='text', placeholder='Title of Conference', required=True),
                    Field(form=paperform, label='Name of Organizer', type='text', placeholder='Name of Organizer', required=True),
                    Field(
                        form=paperform,
                        label='Location of Conference',
                        type='select',
                        required=True,
                        options=[
                            {'value': 'Institutional/In-House', 'label': 'Institutional/In-House'},
                            {'value': 'Local/Regional', 'label': 'Local/Regional'},
                            {'value': 'National', 'label': 'National'},
                            {'value': 'International', 'label': 'International'},
                        ]
                    ),
                    Field(form=paperform, label='Venue, City and Country', type='text', placeholder='Venue, City and Country', required=True),
                    Field(form=paperform, label='Conference Start Date', type='date', required=True),
                    Field(form=paperform, label='Conference End Date', type='date', required=True),
                    Field(form=paperform, label='Date of Presentation', type='date', required=True),
                ]
                paper_presentation_fields_response = Field.objects.bulk_create(paper_presentation_Fields)
                if paper_presentation_fields_response:
                    self.stdout.write("Paper presentation form fields successfully created.")


                patentform = Form.objects.create(title='Patent', creator=user)
                patent_Fields = [
                    Field(form=patentform, label='Title', type='text', placeholder='Title', required=True),
                    Field(form=patentform, label='Patent Title', type='text', placeholder='Title', required=True),
                    Field(
                        form=patentform,
                        label='Type of Patent',
                        type='select',
                        required=True,
                        options=[
                            {'value': 'Invention', 'label': 'Invention'},
                            {'value': 'Utility Model', 'label': 'Utility Model'},
                            {'value': 'Industrial Design', 'label': 'Industrial Design'},
                        ]
                    ),
                    Field(form=patentform, label='Application Number', type='text', placeholder='Application Number', required=True),
                    Field(form=patentform, label='Name of Inventor/s', type='text', placeholder='Name of Inventor/s', required=True),
                    Field(form=patentform, label='Name of Applicant/Owner/s', type='text', placeholder='Name of Applicant/Owner/s', required=True),
                    Field(form=patentform, label='Date of Publication of the Unexamined Application', type='date', required=True),
                    Field(form=patentform, label='Date of Grant of Patent', type='date', placeholder='Leave blank if patent has not been granted.', required=False),
                    Field(form=patentform, label='Registration Number', type='text', placeholder='Leave blank if patent has not been granted.', required=False),
                    Field(
                        form=patentform,
                        label='Name of Commercial Product',
                        type='text',
                        placeholder='Name of Commercial Product',
                        required=False
                    ),
                    Field(
                        form=patentform,
                        label='Use of Patent',
                        type='select',
                        required=True,
                        options=[
                            {'value': 'For development of technology', 'label': 'For development of technology'},
                            {'value': 'For service provision', 'label': 'For service provision'},
                            {'value': 'As an end-product in itself', 'label': 'As an end-product in itself'},
                        ]
                    ),
                ]
                patent_fields_response = Field.objects.bulk_create(patent_Fields)
                if patent_fields_response:
                    self.stdout.write("Patent form fields successfully created.")


                other_researchform = Form.objects.create(title='Other Research', creator=user)
                other_research_Fields = [
                    Field(form=other_researchform, label='Output Title', type='text', required=True),
                    Field(form=other_researchform, label='Type of Output', type='text', required=True),
                    Field(form=other_researchform, label='Type of Public Event', type='text', required=True),
                    Field(form=other_researchform, label='Event Title', type='text', required=True),
                    Field(form=other_researchform, label='Organizer Name', type='text', required=True),
                    Field(form=other_researchform, label='Event Venue', type='text', required=True),
                    Field(form=other_researchform, label='Event Location', type='text', required=True),
                    Field(form=other_researchform, label='Event Start Date', type='date', required=True),
                    Field(form=other_researchform, label='Event End Date', type='date', required=True),
                    Field(form=other_researchform, label='First Shown/Released to Public Date', type='date', required=True),
                    Field(form=other_researchform, label='Industry Utilization', type='text', required=False),
                ]
                other_research_fields_response = Field.objects.bulk_create(other_research_Fields)
                if other_research_fields_response:
                    self.stdout.write("Other research form fields successfully created.")


                trainingform = Form.objects.create(title='Training', creator=user)
                training_Fields = [
                    Field(form=trainingform, label='Title', type='text', required=True),
                    Field(form=trainingform, label='Activity Type', type='text', required=True),
                    Field(form=trainingform, label='Course or Service Title', type='text', required=True),
                    Field(form=trainingform, label='Venue', type='text', required=True),
                    Field(form=trainingform, label='Start Date', type='date', required=True),
                    Field(form=trainingform, label='End Date', type='date', required=True),
                    Field(form=trainingform, label='Schedule Notes', type='text', required=False),
                    Field(form=trainingform, label='Hours Required', type='number', required=False),
                    Field(form=trainingform, label='Number of Trainees Served', type='number', required=False),
                    Field(form=trainingform, label='Source of Funding', type='text', required=False),
                ]
                training_fields_response = Field.objects.bulk_create(training_Fields)
                if training_fields_response:
                    self.stdout.write("Training form fields successfully created.")


                extensionform = Form.objects.create(title='Extension', creator=user)
                extension_Fields = [
                    Field(form=extensionform, label='Title', type='text', required=True),
                    Field(form=extensionform, label='Components', type='text', required=True),
                    Field(form=extensionform, label='Scope', type='text', required=True),
                    Field(form=extensionform, label='Start Date', type='date', required=True),
                    Field(form=extensionform, label='End Date', type='date', required=True),
                    Field(form=extensionform, label='Target Beneficiary Group', type='text', required=True),
                    Field(form=extensionform, label='Beneficiaries Served', type='number', required=False),
                    Field(form=extensionform, label='Source of Funding', type='text', required=False),
                ]
                extension_fields_response = Field.objects.bulk_create(extension_Fields)
                if extension_fields_response:
                    self.stdout.write("Extension form fields successfully created.")


                partnershipform = Form.objects.create(title='Partnership', creator=user)
                partnership_fields = [
                    Field(form=partnershipform, label='Title', type='text', required=True),
                    Field(form=partnershipform, label='Extension Activities under Partnership', type='text', required=True),
                    Field(form=partnershipform, label='Extension Partnership Title', type='text', required=True),
                    Field(form=partnershipform, label='Scope of Work (UP)', type='text', required=True),
                    Field(form=partnershipform, label='Partner/Stakeholder Name', type='text', required=True),
                    Field(form=partnershipform, label='Stakeholder Category', type='text', required=True),
                    Field(form=partnershipform, label='Partnership Agreement Type', type='text', required=True),
                    Field(form=partnershipform, label='Agreement Start Date', type='date', required=True),
                    Field(form=partnershipform, label='Agreement End Date', type='date', required=False),
                ]
                partnership_fields_response = Field.objects.bulk_create(partnership_fields)

                
                othersform = Form.objects.create(title='Others', creator=user)
                others_fields = [
                    Field(form=othersform, label='Title', type='text', required=True),
                    Field(form=othersform, label='Description', type='text', required=True),
                ]
                others_fields_response = Field.objects.bulk_create(others_fields)
                if partnership_fields_response and others_fields_response:
                    self.stdout.write("Partnership and Others forms successfully created.")

        except Exception as e:
            self.stderr.write(f"Failed to create form or fields: {str(e)}")