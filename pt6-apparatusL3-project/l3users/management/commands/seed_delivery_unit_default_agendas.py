from django.core.management.base import BaseCommand
from l3meetings.models import DeliveryUnit, Agenda, DeliveryUnitDefaultAgenda

class Command(BaseCommand):
    help = 'Seed the database with Default Agenda mappings for Delivery Units'

    def handle(self, *args, **kwargs):
        self.stdout.write('Mapping Default Agendas to Delivery Units...')
        
        try:
            # Find the "Open Source" delivery unit
            open_source_du = DeliveryUnit.objects.get(title="Open Source")
        except DeliveryUnit.DoesNotExist:
            self.stdout.write(self.style.ERROR('Delivery Unit "Open Source" does not exist.'))
            return

        # Find all default agendas
        default_agendas = Agenda.objects.filter(is_default=True)
        
        if not default_agendas.exists():
            self.stdout.write(self.style.ERROR('No default agendas found.'))
            return

        # Clear existing mappings
        DeliveryUnitDefaultAgenda.objects.all().delete()

        # Create mappings
        for agenda in default_agendas:
            DeliveryUnitDefaultAgenda.objects.create(
                delivery_unit=open_source_du,
                agenda=agenda
            )

        self.stdout.write(self.style.SUCCESS('Successfully mapped Default Agendas to Delivery Unit "Open Source".'))
