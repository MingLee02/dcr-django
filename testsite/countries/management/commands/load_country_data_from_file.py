import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from .utils import create_region, create_country, create_domain


class Command(BaseCommand):
    help = "Loads country data from a JSON file."

    IMPORT_FILE = os.path.join(
        settings.BASE_DIR, "..", "data", "countries.json"
    )

    def get_data(self):
        with open(self.IMPORT_FILE) as f:
            data = json.load(f)
        return data

    def handle(self, *args, **options):
        data = self.get_data()
        for row in data:
            region = create_region(self, row)

            country = create_country(self, row, region)

            if row.get('topLevelDomain', ' '):
                country.top_level_domain.clear()
                create_domain(self, country, row.get('topLevelDomain', ' '))
