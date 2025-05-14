from django.core.management.base import BaseCommand
from report.models import Form, Field, Report
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

ENTITY_TYPE_OPTIONS = [
    {'value': 'UP_ENTITY', 'label': 'UP Entity'},
    {'value': 'RP_GOVERNMENT_ENTITY_OR_PUBLIC_SECTOR_ENTITY', 'label': 'RP Government Entity or Public Sector Entity'},
    {'value': 'RP_PRIVATE_SECTOR_ENTITY', 'label': 'RP Private Sector Entity'},
    {'value': 'FOREIGN_OR_NONDOMESTIC_ENTITY', 'label': 'Foreign or Non-Domestic Entity'},
]

TYPE_OF_PUBLICATION_OPTIONS = [
    {'value': 'PEER_REVIEWED_JOURNAL_ARTICLE', 'label': 'Peer Reviewed Journal Article'},
    {'value': 'BOOK', 'label': 'Book'},
    {'value': 'EDITED_OR_PEER_REVIEWED_BOOK_CHAPTER', 'label': 'Edited or Peer Reviewed Book Chapter'},
    {'value': 'PEER_REVIEWED_CONFERENCE_PAPER_PUBLICATION', 'label': 'Peer Reviewed Conference Paper Publication'},
    {'value': 'OTHER', 'label': 'Other'},
]

TYPE_OF_PUBLISHER_OPTIONS = [
    {'value': 'COMMERCIAL', 'label': 'Commercial'},
    {'value': 'LEARNED_SOCIETY_AND_ASSOCIATION', 'label': 'Learned Society and Association'},
    {'value': 'UNIVERSITY_PRESS', 'label': 'University Press'},
]

LOCATION_OF_PUBLISHER_OPTIONS = [
    {'value': 'LOCAL', 'label': 'Local'},
    {'value': 'INTERNATIONAL', 'label': 'International'},
]

RESEARCH_TITLE_OPTIONS = [
    {'value': 'Project ISAAC: Isolation, Screening, and Antimicrobial Activity of Compounds from Actinobacteria in Mainit Hot Springs, Cebu, Philippines', 'label': 'Project ISAAC: Isolation, Screening, and Antimicrobial Activity of Compounds from Actinobacteria in Mainit Hot Springs, Cebu, Philippines'},
    {'value': 'An Edge-Based Model of SEIR Epidemics on Static Random Networks', 'label': 'An Edge-Based Model of SEIR Epidemics on Static Random Networks'},
    {'value': 'On dual B-filters and Dual B-subalgebras in a Topolological Dual B-algebra', 'label': 'On dual B-filters and Dual B-subalgebras in a Topolological Dual B-algebra'},
    {'value': 'Survey of Heatwaves in the Philippine Seas', 'label': 'Survey of Heatwaves in the Philippine Seas'},
    {'value': 'Relationship between pearl formation and associated biofouling organisms in the pearl oysters of the Arabian Gulf', 'label': 'Relationship between pearl formation and associated biofouling organisms in the pearl oysters of the Arabian Gulf'},
    {'value': 'Impacts of heatwaves and toxic algal blooms on the physiological performance and future aquaculture of the oysters Ostrea edulis and Magallana (Crassostrea) gigas', 'label': 'Impacts of heatwaves and toxic algal blooms on the physiological performance and future aquaculture of the oysters Ostrea edulis and Magallana (Crassostrea) gigas'},
    {'value': 'River Ecosystem Health Assessment using Biomonitoring Tools', 'label': 'River Ecosystem Health Assessment using Biomonitoring Tools'},
    {'value': 'Other', 'label': 'Other'},
]

TYPE_OF_PRESENTATION_OPTIONS = [
    {'value': 'Oral Presentation', 'label': 'Oral Presentation'},
    {'value': 'Poster Presentation', 'label': 'Poster Presentation'},
]

LOCATION_OF_CONFERENCE_OPTIONS = [
    {'value': 'Institutional/In-House', 'label': 'Institutional/In-House'},
    {'value': 'Local/Regional', 'label': 'Local/Regional'},
    {'value': 'National', 'label': 'National'},
    {'value': 'International', 'label': 'International'},
]

TYPE_OF_PATENT_OPTIONS = [
    {'value': 'Invention', 'label': 'Invention'},
    {'value': 'Utility Model', 'label': 'Utility Model'},
    {'value': 'Industrial Design', 'label': 'Industrial Design'},
]

USE_OF_PATENT_OPTIONS = [
    {'value': 'For development of technology', 'label': 'For development of technology'},
    {'value': 'For service provision', 'label': 'For service provision'},
    {'value': 'As an end-product in itself', 'label': 'As an end-product in itself'},
]

REPORT_TYPE_DESCRIPTIONS = {
    "RESEARCH": 
    """Project/program/work must be part of the approved Research/Creative Work agenda and endorsed by the Dean/Head of Unit and/or approved by the Chancellor/Authorized Official.
Exclude student theses and dissertations.
Researcher/s here refer to full-time faculty members, REPS and staff, whether with permanent, temporary or contractual appointment, who are in service still during the coverage years in review.
Exclude from this data collection those projects/works led by lecturers or non-regular part-time staff.""",
    "PUBLICATION": "Publications may be produced in print, online or in digital on non-print media.",
    "PAPER_PRESENTATION": "The same paper may be presented at different conference events.",
    "PATENT": "Please include only the inventions, utility models and industrial designs owned by the University of the Philippines.",
    "OTHER_RESEARCH": "Include research or creative work outputs that could not be categorized as peer-reviewed publication, academic conference paper presentation or patenting. The output must be exposed in a public event such as exhibitions, public performances, or publication, i.e., when the output was first shown in a public place or released to the public.",
    "TRAINING": "Training Course/Advisory Service must be part of the approved Extension Work Agenda.",
    "EXTENSION": "Extension Program must be part of the approved Extension Work Agenda.",
    "PARTNERSHIP": """The partner stakeholder must be another agency, organization, private company, media or any institution recognized by UP as a partner by means of a MOA, MOU or a partnership agreement.
Extension Activity must be part of the approved Extension Work Agenda.
""",
    "OTHERS": """Include but not limited to the following:
- Teaching Awards
- Authorships (Book/Textbook/Manual/Podcast)
- New Academic Courses/Programs Developed
- Policy papers
- Copyrighted Software Products
- Scientific Meetings/Symposia
- Research Awards/IPAs
- Hosting of Research Conferences
- Public Service Awards
- Attendance in Workshops/Trainings
- Fellowships
- Induction as Fellow in a Professional Society
- Additional Degrees
- Visiting Lecturer/Professor, Researcher
- API activities""",
}

class Command(BaseCommand):
    help = 'Automate adding forms'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        email = "admin@ctrlsolutions.com"

        user, created = User.objects.get_or_create(
            defaults={"email": email}
        )

        if created:
            user.set_password("password123")
            user.save()
            self.stdout.write(f"User created.")
        else:
            self.stdout.write(f"This user already exists. Skipping creation.")

        try:
            with transaction.atomic():

                # RESEARCH
                research_form = Form.objects.create(name='Research', code="RESEARCH", description=REPORT_TYPE_DESCRIPTIONS.get("RESEARCH"), creator=user)
                research_form_fields = [
                    Field(form=research_form, label='Research Project/Program/Work Title', code="report_title", type='text'),
                    Field(form=research_form, label='Number of Months in Original Timeframe', type='number'),
                    Field(form=research_form, label='Start Date', type='date'),
                    Field(form=research_form, label='End Date based on actual completion', type='date'),
                    Field(form=research_form, label='Name of Researcher/s', type='text'),
                    Field(
                        form=research_form,
                        label='Source of Majority Share of this Research Funding',
                        type='select',
                         options=ENTITY_TYPE_OPTIONS
                    ),
                ]

                research_fields_response = Field.objects.bulk_create(research_form_fields)
                if research_fields_response:
                    self.stdout.write("Research form fields successfully created.")
                

                # PUBLICATION AS A RESEARCH OUTPUT
                publication_form = Form.objects.create(name='Publication as a Research Output', code="PUBLICATION", description=REPORT_TYPE_DESCRIPTIONS.get("PUBLICATION"), creator=user)
                publication_form_fields = [
                    Field(form=publication_form, label='Publication Title', type='text', placeholder='title', code="report_title", required=True),
                    Field(form=publication_form, label='Author/Co-Authors', type='text', placeholder='Name', required=True),
                    Field(form=publication_form, label='Published or Accepted for Publication', type='date', required=True),
                    Field(form=publication_form, label='Name of Journal/Book/Conference Publication/Other Publication', type='text', required=True),
                    Field(
                        form=publication_form,
                        label='Type of Publication',
                        type='select',
                        required=True,
                        options=TYPE_OF_PUBLICATION_OPTIONS
                    ),
                    Field(
                        form=publication_form,
                        label='Type of Publisher',
                        type='select',
                        required=True,
                        options=TYPE_OF_PUBLISHER_OPTIONS
                    ),
                    Field(
                        form=publication_form,
                        label='Location of Publisher',
                        type='select',
                        required=True,
                        options=LOCATION_OF_PUBLISHER_OPTIONS
                    ),
                    Field(form=publication_form, label='Volume Number', type='text', required=True),
                    Field(form=publication_form, label='Issue Number', type='text', required=True),
                    Field(form=publication_form, label='Editor Names', type='text', required=True),
                    Field(form=publication_form, label='DOI or URL', type='text', required=True),
                    Field(form=publication_form, label='ISBN or ISSN', type='text', required=True),
                    Field(form=publication_form, label='Number of Citations', type='number', required=True),
                ]

                publication_fields_response = Field.objects.bulk_create(publication_form_fields)
                if publication_fields_response:
                    self.stdout.write("Publication form fields successfully created.")


                # PAPER PRESENTATION AS A RESEARCH OUTPUT
                paper_presentation_form = Form.objects.create(name='Paper Presentation as a Research Output', code="PAPER_PRESENTATION", description=REPORT_TYPE_DESCRIPTIONS.get("PAPER_PRESENTATION"), creator=user)
                paper_presentation_fields = [
                    Field(
                        form=paper_presentation_form,
                        label='Research Project/Program/Work Title',
                        code="report_title",
                        type='select',
                        placeholder='Select Research Title',
                        required=True,
                        options=RESEARCH_TITLE_OPTIONS
                    ),
                    Field(form=paper_presentation_form, label='Title of Paper Presented', type='text', placeholder='Title of Paper Presented', required=True),
                    Field(
                        form=paper_presentation_form,
                        label='Type of Presentation',
                        type='select',
                        required=True,
                        options=TYPE_OF_PRESENTATION_OPTIONS
                    ),
                    Field(form=paper_presentation_form, label='Title of Conference', type='text', placeholder='Title of Conference', required=True),
                    Field(form=paper_presentation_form, label='Name of Organizer', type='text', placeholder='Name of Organizer', required=True),
                    Field(
                        form=paper_presentation_form,
                        label='Location of Conference',
                        type='select',
                        required=True,
                        options=LOCATION_OF_CONFERENCE_OPTIONS
                    ),
                    Field(form=paper_presentation_form, label='Venue, City and Country', type='text', placeholder='Venue, City and Country', required=True),
                    Field(form=paper_presentation_form, label='Conference Start Date', type='date', required=True),
                    Field(form=paper_presentation_form, label='Conference End Date', type='date', required=True),
                    Field(form=paper_presentation_form, label='Date of Presentation', type='date', required=True),
                ]

                paper_presentation_fields_response = Field.objects.bulk_create(paper_presentation_fields)
                if paper_presentation_fields_response:
                    self.stdout.write("Paper presentation form fields successfully created.")

                # PATENT AS A RESEARCH OUTPUT
                patent_form = Form.objects.create(name='Patent as a Research Output', code="PATENT", description=REPORT_TYPE_DESCRIPTIONS.get("PATENT"), creator=user)
                patent_fields = [
                    Field(form=patent_form, label='Title', code="report_title", type='text', placeholder='Title', required=True),
                    Field(form=patent_form, label='Patent Title', type='text', placeholder='Title', required=True),
                    Field(
                        form=patent_form,
                        label='Type of Patent',
                        type='select',
                        required=True,
                        options=TYPE_OF_PATENT_OPTIONS
                    ),
                    Field(form=patent_form, label='Application Number', type='text', placeholder='Application Number', required=True),
                    Field(form=patent_form, label='Name of Inventor/s', type='text', placeholder='Name of Inventor/s', required=True),
                    Field(form=patent_form, label='Name of Applicant/Owner/s', type='text', placeholder='Name of Applicant/Owner/s', required=True),
                    Field(form=patent_form, label='Date of Publication of the Unexamined Application', type='date', required=True),
                    Field(form=patent_form, label='Date of Grant of Patent', type='date', placeholder='Leave blank if patent has not been granted.', required=False),
                    Field(form=patent_form, label='Registration Number', type='text', placeholder='Leave blank if patent has not been granted.', required=False),
                    Field(
                        form=patent_form,
                        label='Name of Commercial Product',
                        type='text',
                        placeholder='Name of Commercial Product',
                        required=False
                    ),
                    Field(
                        form=patent_form,
                        label='Use of Patent',
                        type='select',
                        required=True,
                        options=USE_OF_PATENT_OPTIONS
                    ),
                ]

                patent_fields_response = Field.objects.bulk_create(patent_fields)
                if patent_fields_response:
                    self.stdout.write("Patent form fields successfully created.")

                # OTHER RESEARCH OUTPUT
                other_research_form = Form.objects.create(name='Other Research Output', code="OTHER_RESEARCH", description=REPORT_TYPE_DESCRIPTIONS.get("OTHER_RESEARCH"), creator=user)
                other_research_fields = [
                    Field(form=other_research_form, label='Output Title', code="report_title", type='text', required=True),
                    Field(form=other_research_form, label='Type of Output', type='text', required=True),
                    Field(form=other_research_form, label='Type of Public Event', type='text', required=True),
                    Field(form=other_research_form, label='Event Title', type='text', required=True),
                    Field(form=other_research_form, label='Organizer Name', type='text', required=True),
                    Field(form=other_research_form, label='Event Venue', type='text', required=True),
                    Field(form=other_research_form, label='Event Location', type='text', required=True),
                    Field(form=other_research_form, label='Event Start Date', type='date', required=True),
                    Field(form=other_research_form, label='Event End Date', type='date', required=True),
                    Field(form=other_research_form, label='First Shown/Released to Public Date', type='date', required=True),
                    Field(form=other_research_form, label='Industry Utilization', type='text', required=False),
                ]

                other_research_fields_response = Field.objects.bulk_create(other_research_fields)
                if other_research_fields_response:
                    self.stdout.write("Other research form fields successfully created.")

                # TRAINING COURSE AND/OR ADVISORY SERVICE
                training_advisory_form = Form.objects.create(name='Training Course and/or Advisory Service', code="TRAINING", description=REPORT_TYPE_DESCRIPTIONS.get("TRAINING"), creator=user)
                training_fields = [
                    Field(form=training_advisory_form, label='Title', code="report_title", type='text', required=True),
                    Field(form=training_advisory_form, label='Activity Type', type='text', required=True),
                    Field(form=training_advisory_form, label='Course or Service Title', type='text', required=True),
                    Field(form=training_advisory_form, label='Venue', type='text', required=True),
                    Field(form=training_advisory_form, label='Start Date', type='date', required=True),
                    Field(form=training_advisory_form, label='End Date', type='date', required=True),
                    Field(form=training_advisory_form, label='Schedule Notes', type='text', required=False),
                    Field(form=training_advisory_form, label='Hours Required', type='number', required=False),
                    Field(form=training_advisory_form, label='Number of Trainees Served', type='number', required=False),
                    Field(form=training_advisory_form, label='Source of Funding', type='text', required=False),
                ]

                training_fields_response = Field.objects.bulk_create(training_fields)
                if training_fields_response:
                    self.stdout.write("Training form fields successfully created.")

                # EXTENSION PROGRAM
                extension_form = Form.objects.create(name='Extension Program', code="EXTENSION", description=REPORT_TYPE_DESCRIPTIONS.get("EXTENSION"), creator=user)
                extension_fields = [
                    Field(form=extension_form, label='Title', code="report_title", type='text', required=True),
                    Field(form=extension_form, label='Components', type='text', required=True),
                    Field(form=extension_form, label='Scope', type='text', required=True),
                    Field(form=extension_form, label='Start Date', type='date', required=True),
                    Field(form=extension_form, label='End Date', type='date', required=True),
                    Field(form=extension_form, label='Target Beneficiary Group', type='text', required=True),
                    Field(form=extension_form, label='Beneficiaries Served', type='number', required=False),
                    Field(form=extension_form, label='Source of Funding', type='text', required=False),
                ]

                extension_fields_response = Field.objects.bulk_create(extension_fields)
                if extension_fields_response:
                    self.stdout.write("Extension form fields successfully created.")

                # PARTNERSHIP WITH STAKEHOLDER
                partnership_form = Form.objects.create(name='Partnership with Stakeholder', code="PARTNERSHIP", description=REPORT_TYPE_DESCRIPTIONS.get("PARTNERSHIP"), creator=user)
                partnership_fields = [
                    Field(form=partnership_form, label='Title', code="report_title", type='text', required=True),
                    Field(form=partnership_form, label='Extension Activities under Partnership', type='text', required=True),
                    Field(form=partnership_form, label='Extension Partnership Title', type='text', required=True),
                    Field(form=partnership_form, label='Scope of Work (UP)', type='text', required=True),
                    Field(form=partnership_form, label='Partner/Stakeholder Name', type='text', required=True),
                    Field(form=partnership_form, label='Stakeholder Category', type='text', required=True),
                    Field(form=partnership_form, label='Partnership Agreement Type', type='text', required=True),
                    Field(form=partnership_form, label='Agreement Start Date', type='date', required=True),
                    Field(form=partnership_form, label='Agreement End Date', type='date', required=False),
                ]

                partnership_fields_response = Field.objects.bulk_create(partnership_fields)
                if partnership_fields_response:
                    self.stdout.write("Partnership form successfully created.")

                # OTHERS
                others_form = Form.objects.create(name='Others', code="OTHERS", description=REPORT_TYPE_DESCRIPTIONS.get("OTHERS"), creator=user)
                others_fields = [
                    Field(form=others_form, label='Title', code="report_title", type='text', required=True),
                    Field(form=others_form, label='Description', type='text', required=True),
                ]

                others_fields_response = Field.objects.bulk_create(others_fields)
                if others_fields_response:
                    self.stdout.write("Others form successfully created.")

        except Exception as e:
            self.stderr.write(f"Failed to create form or fields: {str(e)}")