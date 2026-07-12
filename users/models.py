from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        FLEET_MANAGER = "FLEET_MANAGER", "Fleet Manager"
        DRIVER = "DRIVER", "Driver"
        SAFETY_OFFICER = "SAFETY_OFFICER", "Safety Officer"
        FINANCIAL_ANALYST = "FINANCIAL_ANALYST", "Financial Analyst"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.FLEET_MANAGER)
    phone = models.CharField(max_length=20, blank=True)

    def is_fleet_manager(self):
        return self.role == self.Role.FLEET_MANAGER or self.is_superuser

    def is_driver_role(self):
        return self.role == self.Role.DRIVER

    def is_safety_officer(self):
        return self.role == self.Role.SAFETY_OFFICER or self.is_superuser

    def is_financial_analyst(self):
        return self.role == self.Role.FINANCIAL_ANALYST or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
