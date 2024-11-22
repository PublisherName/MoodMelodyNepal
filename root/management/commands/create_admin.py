# myapp/management/commands/create_admin.py

import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create an admin user if it does not exist"

    def handle(self, *args, **kwargs):
        admin_username = os.environ.get("DJANGO_ADMIN_USERNAME")
        admin_password = os.environ.get("DJANGO_ADMIN_PASSWORD")
        admin_email = os.environ.get("DJANGO_ADMIN_EMAIL")

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(admin_username, admin_email, admin_password)
            self.stdout.write(self.style.SUCCESS(f'Admin user "{admin_username}" created'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin user "{admin_username}" already exists'))
