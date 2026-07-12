from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehicle
from .forms import VehicleForm


@login_required
def vehicle_list(request):
    qs = Vehicle.objects.all()
    v_type = request.GET.get("type")
    status = request.GET.get("status")
    region = request.GET.get("region")
    query = request.GET.get("q")
    if v_type:
        qs = qs.filter(vehicle_type=v_type)
    if status:
        qs = qs.filter(status=status)
    if region:
        qs = qs.filter(region__icontains=region)
    if query:
        qs = qs.filter(registration_number__icontains=query) | qs.filter(name__icontains=query)
    return render(request, "vehicles/vehicle_list.html", {
        "vehicles": qs.order_by("-created_at"),
        "type_choices": Vehicle.VehicleType.choices,
        "status_choices": Vehicle.Status.choices,
    })


@login_required
def vehicle_create(request):
    if not request.user.is_fleet_manager():
        messages.error(request, "Only Fleet Managers can register vehicles.")
        return redirect("vehicles:list")
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle registered successfully.")
            return redirect("vehicles:list")
    else:
        form = VehicleForm()
    return render(request, "vehicles/vehicle_form.html", {"form": form, "title": "Register Vehicle"})


@login_required
def vehicle_edit(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if not request.user.is_fleet_manager():
        messages.error(request, "Only Fleet Managers can edit vehicles.")
        return redirect("vehicles:list")
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle updated.")
            return redirect("vehicles:list")
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, "vehicles/vehicle_form.html", {"form": form, "title": "Edit Vehicle"})


@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if not request.user.is_fleet_manager():
        messages.error(request, "Only Fleet Managers can delete vehicles.")
        return redirect("vehicles:list")
    vehicle.delete()
    messages.success(request, "Vehicle deleted.")
    return redirect("vehicles:list")
