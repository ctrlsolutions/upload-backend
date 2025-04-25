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


#  const formInformation = {
#         research: "Project/program/work must be part of the approved Research/Creative Work agenda and endorsed by the Dean/Head of Unit and/or approved by the Chancellor/Authorized Official. Exclude student theses and dissertations. Researcher/s here refer to full-time faculty members, REPS and staff, whether with permanent, temporary or contractual appointment, who are in service still during the coverage years in review. Exclude from this data collection those projects/works led by lecturers or non-regular part-time staff.",
#         publication: "Publications may be produced in print, online or in digital on non-print media.",
#         paper_presentation: "The same paper may be presented at different conference events.",
#         patent: "Please include only the inventions, utility models and industrial designs owned by the University of the Philippines.",
#         other_research: "Include research or creative work outputs that could not be categorized as peer-reviewed publication, academic conference paper presentation or patenting. The output must be exposed in a public event such as exhibitions, public performances, or publication, i.e., when the output was first shown in a public place or released to the public.",
#         training: "Training Course/Advisory Service must be part of the approved Extension Work Agenda.",
#         extension: "Extension Program must be part of the approved Extension Work Agenda.",
#         partnership: "The partner stakeholder must be another agency, organization, private company, media or any institution recognized by UP as a partner by means of a MOA, MOU or a partnership agreement. Extension Activity must be part of the approved Extension Work Agenda.",
#         other: "Other Form",
#     };

# const locfields = {
#         research: [
#             { label: 'Title', model: 'title', component: 'text', placeholder: 'Title', isRequired: true },
#             { 
#                 label: 'Number of Months in Original Timeframe', 
#                 model: 'timeframe', 
#                 component: 'number', 
#                 isRequired: true,
#                 placeholder: 'months'
#             },
#             { label: 'Start Date', model: 'start_date', component: 'date', isRequired: true },
#             { label: 'End Date', model: 'end_date', component: 'date', isRequired: true },
#             { 
#                 label: 'Names of Researchers', 
#                 model: 'names_of_researchers', 
#                 component: 'text', 
#                 isRequired: false,
#                 placeholder: 'Ex: Randall A. Alquicer, Brent Jordan Aguinalde, ...',
            
#             },
#             {
#                 label: 'Source of Majority of Funding', 
#                 model: 'source_of_funding', 
#                 component: 'select', 
#                 isRequired: false, 
#                 options:[
#                     { value: 'up-entity', label: 'Local' },
#                     { value: 'rp-governemnt-entity-or-public-sector-entity', label: 'RP Government Entity or Public Sector Entity' },
#                     { value: 'rp-private-sector-entity', label: 'RP Private Sector Entity' },
#                     { value: 'foreign-or-nondomestic-entity', label: 'Foreign or Non-Domestic Entity' },
#                 ]},
#         ], // [TODO]: name should be arrayed
#         publication: [
#             { label: 'Publication Title', model: 'title', component: 'text', placeholder: 'title', isRequired: true },
#             { label: 'Author/Co-Authors', model: 'author_names', component: 'text', placeholder: 'Name', isRequired: true },
#             { label: 'Published or Accepted for Publication', model: 'publication_date', component: 'date', isRequired: true },
#             { 
#                 label: 'Name of Journal/Book/Conference Publication/Other Publication', 
#                 model: 'publisher_name',
#                 component: 'text',
#                 isRequired: true 
#             },
#             {
#                 label: 'Type of Publication',
#                 model: 'publication_type',
#                 component: 'select',
#                 isRequired: true,
#                 options: [
#                     { value: 'PEER_REVIEWED_JOURNAL_ARTICLE', label: 'Peer Reviewed Journal Article' },
#                     { value: 'BOOK', label: 'Book' },
#                     { value: 'EDITED_OR_PEER_REVIEWED_BOOK_CHAPTER', label: 'Edited or Peer Reviewed Book Chapter' },
#                     { value: 'PEER_REVIEWED_CONFERENCE_PAPER_PUBLICATION', label: 'Peer Reviewed Conference Paper Publication' },
#                     { value: 'OTHER', label: 'Other' },
#                 ]
#             },
#             {
#                 label: 'Type of Publisher',
#                 model: 'publisher_type',
#                 component: 'select',
#                 isRequired: true,
#                 options: [
#                     { value: 'COMMERCIAL', label: 'Commercial' },
#                     { value: 'LEARNED_SOCIETY_AND_ASSOCIATION', label: 'Learned Society and Association' },
#                     { value: 'UNIVERSITY_PRESS', label: 'University Press' },
#                 ]
#             },
#             {
#                 label: 'Location of Publisher',
#                 model: 'publisher_location',
#                 component: 'select',
#                 isRequired: true,
#                 options: [
#                     { value: 'LOCAL', label: 'Local' },
#                     { value: 'INTERNATIONAL', label: 'International' },
#                 ]
#             },
#             { label: 'Volume Number', model: 'volume_number', component: 'text', isRequired: true },
#             { label: 'Issue Number', model: 'issue_number', component: 'text', isRequired: true },
#             { label: 'Editor Names', model: 'editor_names', component: 'text', isRequired: true },
#             { label: 'DOI or URL', model: 'doi_or_url', component: 'text', isRequired: true },
#             { label: 'ISBN or ISSN', model: 'isbn_or_issn', component: 'text', isRequired: true },   
#             { label: 'Number of Citations', model: 'number_of_citations', component: 'number', isRequired: true },
#         ],
#         paper_presentation: [
#             {
#                 label: 'Research Project/Program/Work Title',
#                 model: 'title',
#                 component: 'select',
#                 placeholder: 'Select Research Title',
#                 isRequired: true,
#                 options: [
#                     { value: 'Project ISAAC: Isolation, Screening, and Antimicrobial Activity of Compounds from Actinobacteria in Mainit Hot Springs, Cebu, Philippines', label: 'Project ISAAC: Isolation, Screening, and Antimicrobial Activity of Compounds from Actinobacteria in Mainit Hot Springs, Cebu, Philippines' },
#                     { value: 'An Edge-Based Model of SEIR Epidemics on Static Random Networks', label: 'An Edge-Based Model of SEIR Epidemics on Static Random Networks' },
#                     { value: 'On dual B-filters and Dual B-subalgebras in a Topolological Dual B-algebra', label: 'On dual B-filters and Dual B-subalgebras in a Topolological Dual B-algebra' },
#                     { value: 'Survey of Heatwaves in the Philippine Seas', label: 'Survey of Heatwaves in the Philippine Seas' },
#                     { value: 'Relationship between pearl formation and associated biofouling organisms in the pearl oysters of the Arabian Gulf', label: 'Relationship between pearl formation and associated biofouling organisms in the pearl oysters of the Arabian Gulf' },
#                     { value: 'Impacts of heatwaves and toxic algal blooms on the physiological performance and future aquaculture of the oysters Ostrea edulis and Magallana (Crassostrea) gigas', label: 'Impacts of heatwaves and toxic algal blooms on the physiological performance and future aquaculture of the oysters Ostrea edulis and Magallana (Crassostrea) gigas' },
#                     { value: 'River Ecosystem Health Assessment using Biomonitoring Tools', label: 'River Ecosystem Health Assessment using Biomonitoring Tools' },
#                     { value: 'Other', label: 'Other' },
#                 ]
#             },
#             { label: 'Title of Paper Presented', model: 'presented_paper_title', component: 'text', placeholder: 'Title of Paper Presented', isRequired: true },
#             {
#                 label: 'Type of Presentation',
#                 model: 'presentation_type',
#                 component: 'select',
#                 isRequired: true,
#                 options: [
#                     { value: 'Oral Presentation', label: 'Oral Presentation' },
#                     { value: 'Poster Presentation', label: 'Poster Presentation' },
#                 ]
#             },
#             { label: 'Title of Conference', model: 'conference_title', component: 'text', placeholder: 'Title of Conference', isRequired: true },
#             { label: 'Name of Organizer', model: 'organizer_name', component: 'text', placeholder: 'Name of Organizer', isRequired: true },
#             {
#                 label: 'Location of Conference',
#                 model: 'conference_location',
#                 component: 'select',
#                 isRequired: true,
#                 options: [
#                     { value: 'Institutional/In-House', label: 'Institutional/In-House' },
#                     { value: 'Local/Regional', label: 'Local/Regional' },
#                     { value: 'National', label: 'National' },
#                     { value: 'International', label: 'International' },
#                 ]
#             },
#             { label: 'Venue, City and Country', model: 'venue', component: 'text', placeholder: 'Venue, City and Country', isRequired: true },
#             { label: 'Conference Start Date', model: 'conference_start_date', component: 'date', isRequired: true },
#             { label: 'Conference End Date', model: 'conference_end_date', component: 'date', isRequired: true },
#             { label: 'Date of Presentation', model: 'presentation_date', component: 'date', isRequired: true },
#         ],
#         patent: [
#             { label: 'Title', model: 'title', component: 'text', placeholder: 'Title', isRequired: true },
#             { label: 'Patent Title', model: 'patent_title', component: 'text', placeholder: 'Title', isRequired: true },
#             {
#                 label: 'Type of Patent',
#                 model: 'patent_type',
#                 component: 'select',
#                 isRequired: true,
#                 options: [
#                     { value: 'Invention', label: 'Invention' },
#                     { value: 'Utility Model', label: 'Utility Model' },
#                     { value: 'Industrial Design', label: 'Industrial Design' },
#                 ]
#             },
#             { label: 'Application Number', model: 'application_no', component: 'text', placeholder: 'Application Number', isRequired: true },
#             { label: 'Name of Inventor/s', model: 'inventors_name', component: 'text', placeholder: 'Name of Inventor/s', isRequired: true },
#             { label: 'Name of Applicant/Owner/s', model: 'owner_name', component: 'text', placeholder: 'Name of Applicant/Owner/s', isRequired: true },
#             { label: 'Date of Publication of the Unexamined Application', model: 'publication_date', component: 'date', isRequired: true },
#             { label: 'Date of Grant of Patent', model: 'grant_date', component: 'date', placeholder: 'Leave blank if patent has not been granted.', isRequired: false },
#             { label: 'Registration Number', model: 'registration_number', component: 'text', placeholder: 'Leave blank if patent has not been granted.', isRequired: false },
#             {
#                 label: 'Name of Commercial Product',
#                 model: 'commercial_product_name',
#                 component: 'text',
#                 placeholder: 'Name of Commercial Product',
#                 isRequired: false
#             },
#             {
#                 label: 'Use of Patent',
#                 model: 'patent_use',
#                 component: 'select',
#                 isRequired: true,
#                 options: [
#                     { value: 'For development of technology', label: 'For development of technology' },
#                     { value: 'For service provision', label: 'For service provision' },
#                     { value: 'As an end-product in itself', label: 'As an end-product in itself' },
#                 ]
#             },
#         ], // [TODO]: bug on title input
#         other_research: [
#             { label: 'Output Title', model: 'title', component: 'text', isRequired: true },
#             { label: 'Type of Output', model: 'output_type', component: 'text', isRequired: true },
#             { label: 'Type of Public Event', model: 'public_event_type', component: 'text', isRequired: true },
#             { label: 'Event Title', model: 'event_title', component: 'text', isRequired: true },
#             { label: 'Organizer Name', model: 'organizer_name', component: 'text', isRequired: true },
#             { label: 'Event Venue', model: 'event_venue', component: 'text', isRequired: true },
#             { label: 'Event Location', model: 'event_location', component: 'text', isRequired: true },
#             { label: 'Event Start Date', model: 'event_start_date', component: 'date', isRequired: true },
#             { label: 'Event End Date', model: 'event_end_date', component: 'date', isRequired: true },
#             { label: 'First Shown/Released to Public Date', model: 'output_firstshownorreleasedtopublic_date', component: 'date', isRequired: true },
#             { label: 'Industry Utilization', model: 'industry_utilization', component: 'text', isRequired: false },
#         ],
#         training: [
#             { label: 'Title', model: 'title', component: 'text', placeholder: 'Title', isRequired: true },
#             { label: 'Activity Type', model: 'activity_type', component: 'text', isRequired: true },
#             { label: 'Course or Service Title', model: 'course_or_service_title', component: 'text', isRequired: true },
#             { label: 'Venue', model: 'venue', component: 'text', isRequired: true },
#             { label: 'Start Date', model: 'start_date', component: 'date', isRequired: true },
#             { label: 'End Date', model: 'end_date', component: 'date', isRequired: true },
#             { label: 'Schedule Notes', model: 'schedule_special_notes', component: 'text', isRequired: false },
#             { label: 'Hours Required', model: 'hours_required_to_complete', component: 'number', isRequired: false },
#             { label: 'Number of Trainees Served', model: 'number_of_trainees_served', component: 'number', isRequired: false },
#             { label: 'Source of Funding', model: 'source_of_funding', component: 'text', isRequired: false },
#         ],
#         extension: [
#             { label: 'Title', model: 'title', component: 'text', placeholder: 'Title', isRequired: true },
#             { label: 'Components', model: 'components', component: 'text', isRequired: true },
#             { label: 'Scope', model: 'scope', component: 'text', isRequired: true },
#             { label: 'Start Date', model: 'start_date', component: 'date', isRequired: true },
#             { label: 'End Date', model: 'end_date', component: 'date', isRequired: true },
#             { label: 'Target Beneficiary Group', model: 'target_beneficiary_group', component: 'text', isRequired: true },
#             { label: 'Beneficiaries Served', model: 'tbg_served', component: 'number', isRequired: false },
#             { label: 'Source of Funding', model: 'source_of_funding', component: 'text', isRequired: false },
#         ],
#         partnership: [
#             { label: 'Title', model: 'title', component: 'text', placeholder: 'Title', isRequired: true },
#             { label: 'Extension Activities under Partnership', model: 'type_of_extension_activities_under_this_partnership', component: 'text', isRequired: true },
#             { label: 'Extension Partnership Title', model: 'extension_partnership_title', component: 'text', isRequired: true },
#             { label: 'Scope of Work (UP)', model: 'up_scope_of_work', component: 'text', isRequired: true },
#             { label: 'Partner/Stakeholder Name', model: 'partner_stakeholder_name', component: 'text', isRequired: true },
#             { label: 'Stakeholder Category', model: 'stakeholder_category', component: 'text', isRequired: true },
#             { label: 'Partnership Agreement Type', model: 'partnership_agreement_type', component: 'text', isRequired: true },
#             { label: 'Agreement Start Date', model: 'partnership_agreement_effectivity_start_date', component: 'date', isRequired: true },
#             { label: 'Agreement End Date', model: 'partnership_agreement_effectivity_end_date', component: 'date', isRequired: false },
#         ],
#         others: [
#             { label: 'Title', model: 'title', component: 'text', placeholder: 'Title', isRequired: true },
#             { label: 'Description', model: 'description', component: 'text', isRequired: true },
#         ],

#     }