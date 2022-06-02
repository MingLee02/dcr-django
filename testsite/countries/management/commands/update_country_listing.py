import json
import os
import requests

from django.core.management.base import BaseCommand

from .utils import create_region, create_country, create_domain


class Command(BaseCommand):
    help = "Loads country data from a url"

    def __init__(
        self, url=None, *args, **kwargs
    ):
        super(Command, self).__init__(*args, **kwargs)
        if not url:
            url = "https://storage.googleapis.com/dcr-django-test/countries.json"
        self._url = url

    def get_data(self):
        request = requests.get(self._url)
        if request.status_code == 200:
            records = json.loads(request._content)
            for record in records:
                yield record
        return None

    def handle(self, *args, **options):
        data = self.get_data()
        if data:
            for row in data:
                region = create_region(self, row)

                country = create_country(self, row, region)

                if row.get('topLevelDomain', ' '):
                    country.top_level_domain.clear()
                    create_domain(
                        self,
                        country,
                        row.get('topLevelDomain', ' ')
                    )
        else:
            self.stdout.write(
                self.style.Error(
                    "No data obtained from the url."
                )
            )
