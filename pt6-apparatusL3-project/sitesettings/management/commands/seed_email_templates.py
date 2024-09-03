# your_app/management/commands/seed_email_templates.py

from django.core.management.base import BaseCommand
from sitesettings.models import *
from sitesettings.email_templates import TEMPLATES
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds the database with initial email templates or updates them if they already exist'

    def handle(self, *args, **options):
        for template in TEMPLATES:
            # Check if the template already exists
            obj, created = EmailNotificationTemplate.objects.update_or_create(
                name=template['name'],
                slug=slugify(template['name']),
                defaults={
                    'subject': template['subject'],
                    'body': template['body'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created template: {template["name"]}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated template: {template["name"]}'))
