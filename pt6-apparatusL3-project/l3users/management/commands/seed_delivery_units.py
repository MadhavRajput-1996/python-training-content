# seed_agendas.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from l3meetings.models import DeliveryUnit

class Command(BaseCommand):
    help = 'Seed the database with Deafult Delivery Unit data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Delivery Units...')
 
        # Clear existing data
        DeliveryUnit.objects.all().delete()

        # Create sample data
        dus = [
            ("Open Source", "Default description for Open Source"),
        ]

        for title, description in dus:
            DeliveryUnit.objects.create(
                title=title,
                description=description,
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded Delivery Units.'))
