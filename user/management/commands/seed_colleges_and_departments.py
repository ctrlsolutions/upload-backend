# yourapp/management/commands/seed_colleges_and_departments.py
from django.core.management.base import BaseCommand
from user.models import College, Department  # Adjust imports based on your model locations

class Command(BaseCommand):
    help = 'Seeds the database with initial colleges and departments'

    def handle(self, *args, **kwargs):
        # College and Department data
        college_data = {
            "COS": {
                "name": "College of Science",
                "departments": {
                    "DCS": "Department of Computer Science",
                    "DBES": "Department of Biology and Environmental Science",
                    "MSP": "Mathematics and Statistics Program"
                }
            },
            "CCAD": {
                "name": "College of Communication, Art and Design",
                "departments": {
                    "COMM": "Communications",
                    "FA": "Fine Arts"
                }
            },
            "SOM": {
                "name": "School of Management",
                "departments": {
                    "MAN": "Management"
                }
            },
            "CSS": {
                "name": "College of Social Science",
                "departments": {
                    "PSY": "Psychology",
                    "AASS": "Sports Studies",
                    "POL": "Political Science"
                }
            }
        }

        # Iterate over each college and create it with its departments
        for college_code, college_info in college_data.items():
            college = College.objects.create(code=college_code, name=college_info["name"])
            for dept_code, dept_name in college_info["departments"].items():
                Department.objects.create(code=dept_code, name=dept_name, college=college)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with colleges and departments'))
