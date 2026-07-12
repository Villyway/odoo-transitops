from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import FuelLog
from .forms import FuelLogForm


@login_required
def fuel_list(request):
    logs = FuelLog.objects.select_related("vehicle").order_by("-date")
    return render(request, "fuel/fuel_list.html", {"logs": logs})


@login_required
def fuel_create(request):
    if request.method == "POST":
        form = FuelLogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fuel log recorded.")
            return redirect("fuel:list")
    else:
        form = FuelLogForm()
    return render(request, "fuel/fuel_form.html", {"form": form, "title": "Record Fuel Log"})
