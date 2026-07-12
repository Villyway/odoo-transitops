from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("id", "source", "destination", "vehicle", "driver", "status", "cargo_weight_kg")
    list_filter = ("status",)
