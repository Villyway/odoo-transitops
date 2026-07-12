from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import transaction

from .models import MaintenanceLog
from .forms import MaintenanceCreateForm
from vehicles.models import Vehicle


@login_required
def maintenance_list(request):
    qs = MaintenanceLog.objects.select_related("vehicle").all()
    status = request.GET.get("status")
    if status:
        qs = qs.filter(status=status)
    return render(request, "maintenance/maintenance_list.html", {
        "logs": qs.order_by("-date_reported"),
        "status_choices": MaintenanceLog.Status.choices,
    })


@login_required
@transaction.atomic
def maintenance_create(request):
    if request.method == "POST":
        form = MaintenanceCreateForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.status = MaintenanceLog.Status.OPEN
            log.save()

            vehicle = log.vehicle
            if vehicle.status != Vehicle.Status.RETIRED:
                vehicle.status = Vehicle.Status.IN_SHOP
                vehicle.save()

            messages.success(request, f"Maintenance record created. {vehicle.registration_number} moved to In Shop.")
            return redirect("maintenance:list")
    else:
        form = MaintenanceCreateForm()
    return render(request, "maintenance/maintenance_form.html", {"form": form, "title": "New Maintenance Record"})


@login_required
@transaction.atomic
def maintenance_close(request, pk):
    log = get_object_or_404(MaintenanceLog, pk=pk)
    if log.status == MaintenanceLog.Status.CLOSED:
        messages.info(request, "This maintenance record is already closed.")
        return redirect("maintenance:list")

    log.status = MaintenanceLog.Status.CLOSED
    log.date_closed = timezone.now().date()
    log.save()

    vehicle = log.vehicle
    still_open = MaintenanceLog.objects.filter(vehicle=vehicle, status=MaintenanceLog.Status.OPEN).exclude(pk=log.pk).exists()
    if not still_open and vehicle.status != Vehicle.Status.RETIRED:
        vehicle.status = Vehicle.Status.AVAILABLE
        vehicle.save()

    messages.success(request, f"Maintenance closed. {vehicle.registration_number} restored to Available (unless retired).")
    return redirect("maintenance:list")
