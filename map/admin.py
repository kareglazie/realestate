from django.contrib import admin
from .models import ConstructionSite, Attraction


@admin.register(ConstructionSite)
class ConstructionSiteAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "developer", "start_date"]
    list_filter = ["status"]
    search_fields = ["name", "developer"]


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "category", "address"]
    list_filter = ["type"]
    search_fields = ["name", "category"]
