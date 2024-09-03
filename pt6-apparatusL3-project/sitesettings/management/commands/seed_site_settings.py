from django.core.management.base import BaseCommand
from sitesettings.models import SiteSettings

class Command(BaseCommand):
    help = 'Seed the database with deafult site data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding site settings...')
        SiteSettings.objects.all().delete()
        initial_data = [
            ('site_name', 'Apparatus L3'),
            ('copyright_text', 'InfoBeans'),
            ('holiday_list', '01-26, 03-14, 05-01, 08-15, 09-17, 10-02, 10-12, 10-31, 11-01, 12-25'),
            ('allow_email_send', 0),
            ('default_meeting_title', 'L3 Meeting For')
        ]

        for k, v in initial_data:
            SiteSettings.objects.create(
                key=k,
                value=v,
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded site settings.'))
