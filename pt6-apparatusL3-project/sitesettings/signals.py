from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.core.management import call_command


@receiver(post_migrate)
def run_seeders(sender, **kwargs):
    call_command('seed_site_settings')
    call_command('seed_email_templates')