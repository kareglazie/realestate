from django.contrib import admin
from .models import ConstructionSite


@admin.register(ConstructionSite)
class ConstructionSiteAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "developer", "start_date"]
    list_filter = ["status", "developer"]
    search_fields = ["name", "developer"]
    list_editable = ["status"]
