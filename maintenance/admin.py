from django.contrib import admin
from .models import MaintenanceLog


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "title", "status", "cost", "date_reported", "date_closed")
    list_filter = ("status",)
