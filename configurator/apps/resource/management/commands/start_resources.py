from django.core.management.base import BaseCommand
from configurator.start import start

class Command(BaseCommand):
    help = 'Starts configured setup'

    def handle(self, *args, **options):
        start()
