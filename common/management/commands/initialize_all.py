from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run all feed/setup commands for initialization'

    def handle(self, *args, **options):
        self.stdout.write("Initializing colleges and departments...")
        call_command('seed_colleges_and_departments')
        
        self.stdout.write("Initializing roles and permissions...")
        call_command('seed_roles_and_permissions')
        
        self.stdout.write("Initializing forms...")
        call_command('seed_existing_forms')

        self.stdout.write(self.style.SUCCESS("All initialization commands ran successfully!"))
