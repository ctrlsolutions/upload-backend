from django.db import migrations

def create_initial_colleges_and_departments(apps, schema_editor):
    College = apps.get_model('user', 'College')
    Department = apps.get_model('user', 'Department')

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

    for college_code, college_info in college_data.items():
        college = College.objects.create(code=college_code, name=college_info["name"])
        for dept_code, dept_name in college_info["departments"].items():
            Department.objects.create(code=dept_code, name=dept_name, college=college)


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_initialize_roles_and_permissions'),
    ]

    operations = [
        migrations.RunPython(create_initial_colleges_and_departments),
    ]
