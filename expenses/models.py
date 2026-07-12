from django.db import models
from vehicles.models import Vehicle


class Expense(models.Model):
    class Category(models.TextChoices):
        TOLL = "TOLL", "Toll"
        PARKING = "PARKING", "Parking"
        FINE = "FINE", "Fine"
        INSURANCE = "INSURANCE", "Insurance"
        OTHER = "OTHER", "Other"

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="expenses")
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    notes = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.get_category_display()} - {self.amount}"
