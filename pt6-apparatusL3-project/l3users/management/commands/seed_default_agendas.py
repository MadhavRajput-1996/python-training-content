# seed_agendas.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from l3meetings.models import Agenda

class Command(BaseCommand):
    help = 'Seed the database with Agenda data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Agendas...')
        
        # Ensure there is at least one admin user

        # Clear existing data
        Agenda.objects.all().delete()

        # Create sample data
        agendas = [
            'Open items of previous L3 Meeting',
            'Key points of L4 meeting',
            'L2 Updates',
            'New Learnings',
        ]

        for title in agendas:
            Agenda.objects.create(
                title=title,
                is_default=True,
                status = 'open'
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded Agendas.'))
