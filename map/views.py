from django.shortcuts import render
from django.core.serializers import serialize
from .models import ConstructionSite, Attraction


def map_view(request):
    sites = ConstructionSite.objects.all()
    attractions = Attraction.objects.all()

    sites_data = []
    for site in sites:
        sites_data.append(
            {
                "name": site.name,
                "description": site.description,
                "latitude": site.latitude,
                "longitude": site.longitude,
                "status": site.status,
                "developer": site.developer,
                "start_date": (
                    site.start_date.strftime("%d.%m.%Y") if site.start_date else None
                ),
                "completion_date": (
                    site.completion_date.strftime("%d.%m.%Y")
                    if site.completion_date
                    else None
                ),
                "phone": site.phone,
                "photos": [],
                "type": "construction",
            }
        )

    attractions_data = []
    for attraction in attractions:
        attractions_data.append(
            {
                "name": attraction.name,
                "description": attraction.description,
                "latitude": attraction.latitude,
                "longitude": attraction.longitude,
                "category": attraction.category,
                "address": attraction.address,
                "working_hours": attraction.working_hours,
                "website": attraction.website,
                "phone": attraction.phone,
                "type": "attraction",
                "attraction_type": attraction.type,
            }
        )

    all_objects = sites_data + attractions_data

    return render(
        request,
        "map/map.html",
        {
            "sites": all_objects,
            "sites_count": len(sites_data),
            "attractions_count": len(attractions_data),
        },
    )
