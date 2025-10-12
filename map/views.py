from django.shortcuts import render
from django.core.serializers import serialize
from .models import ConstructionSite


def map_view(request):
    sites = ConstructionSite.objects.all()

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
            }
        )

    return render(request, "map/map.html", {"sites": sites_data})
