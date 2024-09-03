from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings

class Command(BaseCommand):
    help = 'Seed the database with SocialApp data for social login'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Social Apps...')
        current_domain = settings.CURRENT_DOMAIN
                # List of sites to create
        sites_data = [
            {'domain': current_domain, 'name': current_domain},
            # Add more sites if needed
        ]
        
        sites = []
        for site_data in sites_data:
            site, created = Site.objects.get_or_create(
                domain=site_data['domain'],
                defaults={'name': site_data['name']}
            )
            sites.append(site)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created site: {site_data["domain"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Site already exists: {site_data["domain"]}'))

        
        # List of social applications to create
        if settings.GOOGLE_CLIENT_ID=='' or  settings.GOOGLE_CLIENT_ID=='':
            self.stdout.write(self.style.ERROR('Client id and Client Secret key are required'))
            return

        social_apps = [
            {
                'provider': 'google',
                'name': 'Google',
                'client_id': settings.GOOGLE_CLIENT_ID,
                'secret': settings.GOOGLE_SECRET_KEY,
            },
            # Add more providers if needed
        ]

        for app_data in social_apps:
            app, created = SocialApp.objects.get_or_create(
                provider=app_data['provider'],
                name=app_data['name'],
                defaults={
                    'client_id': app_data['client_id'],
                    'secret': app_data['secret'],
                }
            )
            app.sites.set(sites)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created {app_data["name"]} SocialApp'))
            else:
                self.stdout.write(self.style.WARNING(f'{app_data["name"]} SocialApp already exists'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded Social Apps.'))
