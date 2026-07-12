from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Trip
from .forms import TripCreateForm, TripCompleteForm
from vehicles.models import Vehicle
from drivers.models import Driver
from fuel.models import FuelLog


@login_required
def trip_list(request):
    qs = Trip.objects.select_related("vehicle", "driver").all()
    status = request.GET.get("status")
    if status:
        qs = qs.filter(status=status)
    return render(request, "trips/trip_list.html", {
        "trips": qs.order_by("-created_at"),
        "status_choices": Trip.Status.choices,
    })


@login_required
def trip_create(request):
    if request.method == "POST":
        form = TripCreateForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.created_by = request.user
            trip.status = Trip.Status.DRAFT
            trip.save()
            messages.success(request, "Trip created as Draft.")
            return redirect("trips:list")
    else:
        form = TripCreateForm()
    return render(request, "trips/trip_form.html", {"form": form, "title": "Create Trip"})


@login_required
@transaction.atomic
def trip_dispatch(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if trip.status != Trip.Status.DRAFT:
        messages.error(request, "Only Draft trips can be dispatched.")
        return redirect("trips:list")

    vehicle = trip.vehicle
    driver = trip.driver

    # Re-validate business rules at dispatch time (state may have changed)
    if vehicle.status != Vehicle.Status.AVAILABLE:
        messages.error(request, f"Vehicle {vehicle.registration_number} is no longer available.")
        return redirect("trips:list")
    if driver.status != Driver.Status.AVAILABLE or driver.license_is_expired():
        messages.error(request, f"Driver {driver.name} is not available (suspended/expired license).")
        return redirect("trips:list")
    if trip.cargo_weight_kg > vehicle.max_load_capacity_kg:
        messages.error(request, "Cargo weight exceeds vehicle capacity.")
        return redirect("trips:list")

    trip.status = Trip.Status.DISPATCHED
    trip.dispatched_at = timezone.now()
    trip.save()

    vehicle.status = Vehicle.Status.ON_TRIP
    vehicle.save()

    driver.status = Driver.Status.ON_TRIP
    driver.save()

    messages.success(request, f"Trip #{trip.id} dispatched. Vehicle & Driver marked On Trip.")
    return redirect("trips:list")


@login_required
@transaction.atomic
def trip_complete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if trip.status != Trip.Status.DISPATCHED:
        messages.error(request, "Only Dispatched trips can be completed.")
        return redirect("trips:list")

    if request.method == "POST":
        form = TripCompleteForm(request.POST, instance=trip)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.status = Trip.Status.COMPLETED
            trip.completed_at = timezone.now()
            trip.save()

            vehicle = trip.vehicle
            if trip.final_odometer_km:
                vehicle.odometer_km = trip.final_odometer_km
            vehicle.status = Vehicle.Status.AVAILABLE
            vehicle.save()

            driver = trip.driver
            driver.status = Driver.Status.AVAILABLE
            driver.save()

            if trip.fuel_consumed_liters:
                FuelLog.objects.create(
                    vehicle=vehicle,
                    trip=trip,
                    liters=trip.fuel_consumed_liters,
                    cost=0,
                    date=timezone.now().date(),
                    notes=f"Auto-logged from Trip #{trip.id} completion",
                )

            messages.success(request, f"Trip #{trip.id} completed. Vehicle & Driver marked Available.")
            return redirect("trips:list")
    else:
        form = TripCompleteForm(instance=trip)
    return render(request, "trips/trip_complete.html", {"form": form, "trip": trip})


@login_required
@transaction.atomic
def trip_cancel(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if trip.status not in (Trip.Status.DRAFT, Trip.Status.DISPATCHED):
        messages.error(request, "Trip cannot be cancelled from its current state.")
        return redirect("trips:list")

    was_dispatched = trip.status == Trip.Status.DISPATCHED
    trip.status = Trip.Status.CANCELLED
    trip.save()

    if was_dispatched:
        vehicle = trip.vehicle
        if vehicle.status == Vehicle.Status.ON_TRIP:
            vehicle.status = Vehicle.Status.AVAILABLE
            vehicle.save()
        driver = trip.driver
        if driver.status == Driver.Status.ON_TRIP:
            driver.status = Driver.Status.AVAILABLE
            driver.save()

    messages.success(request, f"Trip #{trip.id} cancelled.")
    return redirect("trips:list")
