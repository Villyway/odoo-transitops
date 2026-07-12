from django.db import models
from vehicles.models import Vehicle


class MaintenanceLog(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        CLOSED = "CLOSED", "Closed"

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="maintenance_logs")
    title = models.CharField(max_length=150, help_text="e.g. Oil Change, Brake Repair")
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    date_reported = models.DateField(auto_now_add=True)
    date_closed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.title} ({self.status})"
