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

        Forms = [
            Form(title='Form 1', creator=user),
            Form(title='Form 2', creator=user)
        ]   
        Form.objects.bulk_create(Forms)
 
