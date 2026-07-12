from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Driver
from .forms import DriverForm


@login_required
def driver_list(request):
    qs = Driver.objects.all()
    status = request.GET.get("status")
    query = request.GET.get("q")
    if status:
        qs = qs.filter(status=status)
    if query:
        qs = qs.filter(name__icontains=query) | qs.filter(license_number__icontains=query)
    return render(request, "drivers/driver_list.html", {
        "drivers": qs.order_by("-created_at"),
        "status_choices": Driver.Status.choices,
    })


@login_required
def driver_create(request):
    if not (request.user.is_fleet_manager() or request.user.is_safety_officer()):
        messages.error(request, "Only Fleet Managers/Safety Officers can add drivers.")
        return redirect("drivers:list")
    if request.method == "POST":
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver added successfully.")
            return redirect("drivers:list")
    else:
        form = DriverForm()
    return render(request, "drivers/driver_form.html", {"form": form, "title": "Add Driver"})


@login_required
def driver_edit(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if not (request.user.is_fleet_manager() or request.user.is_safety_officer()):
        messages.error(request, "Only Fleet Managers/Safety Officers can edit drivers.")
        return redirect("drivers:list")
    if request.method == "POST":
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver updated.")
            return redirect("drivers:list")
    else:
        form = DriverForm(instance=driver)
    return render(request, "drivers/driver_form.html", {"form": form, "title": "Edit Driver"})


@login_required
def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if not request.user.is_fleet_manager():
        messages.error(request, "Only Fleet Managers can delete drivers.")
        return redirect("drivers:list")

    pending_trips = driver.trips.count()
    if pending_trips:
        messages.error(
            request,
            f"Cannot delete driver because {pending_trips} trip(s) still reference this driver. "
            "Reassign or remove the trips first."
        )
        return redirect("drivers:list")

    try:
        driver.delete()
        messages.success(request, "Driver deleted.")
    except ProtectedError:
        messages.error(
            request,
            "This driver cannot be deleted because there are protected trip references. "
            "Please clear associated trips before deleting."
        )
    return redirect("drivers:list")
