from django.db.models import Count, Sum
from django.http import JsonResponse

from .models import Country


def get_region_data():
    return Country.objects.all().values(
        'region__name'
    ).annotate(
        number_countries=Count('region_id')
    ).annotate(total_population=Sum('population')).order_by('region__name')


def stats(request):
    region_data = get_region_data()
    if not region_data:
        return JsonResponse({
            "message": "No region data available"
        })

    response = {"regions": [
            {
                'name': data['region__name'],
                'number_countries': data['number_countries'],
                'total_population': data['total_population']
            }
            for data in region_data
        ]
    }

    return JsonResponse(response)
