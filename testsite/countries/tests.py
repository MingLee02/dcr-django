from django.test import TestCase

from .models import Country, Region
from .views import get_region_data


class CountryTestCase(TestCase):
    def setUp(self):
        region = Region.objects.create(name='REGION')
        Country.objects.create(name="country 1", population="10", region=region)
        Country.objects.create(name="country 2", population="30", region=region)

    def test_get_region_data(self):
        """
        Assert that get_region_data correctly returns number of countries tied to a region
        plus the sum of the population
        """
        data = get_region_data()
        data = data.first()

        assert data == {'number_countries': 2, 'region__name': 'REGION', 'total_population': 40}