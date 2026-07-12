import csv
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum, Count, Q

from vehicles.models import Vehicle
from drivers.models import Driver
from trips.models import Trip
from maintenance.models import MaintenanceLog
from fuel.models import FuelLog
from expenses.models import Expense


@login_required
def home(request):
    v_type = request.GET.get("type")
    status = request.GET.get("status")
    region = request.GET.get("region")

    vehicles = Vehicle.objects.all()
    if v_type:
        vehicles = vehicles.filter(vehicle_type=v_type)
    if status:
        vehicles = vehicles.filter(status=status)
    if region:
        vehicles = vehicles.filter(region__icontains=region)

    total_vehicles = vehicles.count()
    active_vehicles = vehicles.exclude(status=Vehicle.Status.RETIRED).count()
    available_vehicles = vehicles.filter(status=Vehicle.Status.AVAILABLE).count()
    in_maintenance = vehicles.filter(status=Vehicle.Status.IN_SHOP).count()
    on_trip_vehicles = vehicles.filter(status=Vehicle.Status.ON_TRIP).count()

    active_trips = Trip.objects.filter(status=Trip.Status.DISPATCHED).count()
    pending_trips = Trip.objects.filter(status=Trip.Status.DRAFT).count()
    drivers_on_duty = Driver.objects.filter(status=Driver.Status.ON_TRIP).count()

    fleet_utilization = round((on_trip_vehicles / total_vehicles * 100), 2) if total_vehicles else 0
    available_pct = round((available_vehicles / total_vehicles * 100), 2) if total_vehicles else 0
    maintenance_pct = round((in_maintenance / total_vehicles * 100), 2) if total_vehicles else 0
    on_trip_pct = round((on_trip_vehicles / total_vehicles * 100), 2) if total_vehicles else 0
    total_trips = active_trips + pending_trips
    active_trips_pct = round((active_trips / total_trips * 100), 2) if total_trips else 0
    pending_trips_pct = round((pending_trips / total_trips * 100), 2) if total_trips else 0
    new_vehicles = 0

    context = {
        "total_vehicles": total_vehicles,
        "active_vehicles": active_vehicles,
        "available_vehicles": available_vehicles,
        "in_maintenance": in_maintenance,
        "on_trip_vehicles": on_trip_vehicles,
        "active_trips": active_trips,
        "pending_trips": pending_trips,
        "drivers_on_duty": drivers_on_duty,
        "fleet_utilization": fleet_utilization,
        "available_pct": available_pct,
        "maintenance_pct": maintenance_pct,
        "on_trip_pct": on_trip_pct,
        "active_trips_pct": active_trips_pct,
        "pending_trips_pct": pending_trips_pct,
        "new_vehicles": new_vehicles,
        "type_choices": Vehicle.VehicleType.choices,
        "status_choices": Vehicle.Status.choices,
        "regions": Vehicle.objects.exclude(region="").values_list("region", flat=True).distinct(),
    }
    return render(request, "dashboard/home.html", context)


def _vehicle_report_rows():
    rows = []
    for v in Vehicle.objects.all():
        total_fuel = v.fuel_logs.aggregate(l=Sum("liters"), c=Sum("cost"))
        total_fuel_liters = total_fuel["l"] or 0
        total_fuel_cost = total_fuel["c"] or 0
        total_maintenance_cost = v.maintenance_logs.aggregate(c=Sum("cost"))["c"] or 0
        total_expense_cost = v.expenses.aggregate(c=Sum("amount"))["c"] or 0
        total_distance = Trip.objects.filter(vehicle=v, status=Trip.Status.COMPLETED).aggregate(
            d=Sum("planned_distance_km"))["d"] or 0
        total_revenue = Trip.objects.filter(vehicle=v, status=Trip.Status.COMPLETED).aggregate(
            r=Sum("revenue"))["r"] or 0

        operational_cost = total_fuel_cost + total_maintenance_cost + total_expense_cost
        fuel_efficiency = round(float(total_distance) / float(total_fuel_liters), 2) if total_fuel_liters else 0
        roi = None
        if v.acquisition_cost:
            roi = round(float(total_revenue - operational_cost) / float(v.acquisition_cost) * 100, 2)

        rows.append({
            "vehicle": v,
            "total_fuel_liters": total_fuel_liters,
            "total_fuel_cost": total_fuel_cost,
            "total_maintenance_cost": total_maintenance_cost,
            "total_expense_cost": total_expense_cost,
            "operational_cost": operational_cost,
            "total_distance": total_distance,
            "fuel_efficiency": fuel_efficiency,
            "total_revenue": total_revenue,
            "roi_percent": roi,
        })
    return rows


@login_required
def reports(request):
    rows = _vehicle_report_rows()
    return render(request, "dashboard/reports.html", {"rows": rows})


@login_required
def reports_csv_export(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="transitops_report.csv"'
    writer = csv.writer(response)
    writer.writerow([
        "Registration Number", "Vehicle Name", "Total Distance (km)", "Total Fuel (L)",
        "Fuel Cost", "Maintenance Cost", "Other Expenses", "Total Operational Cost",
        "Fuel Efficiency (km/L)", "Revenue", "ROI (%)"
    ])
    for row in _vehicle_report_rows():
        writer.writerow([
            row["vehicle"].registration_number,
            row["vehicle"].name,
            row["total_distance"],
            row["total_fuel_liters"],
            row["total_fuel_cost"],
            row["total_maintenance_cost"],
            row["total_expense_cost"],
            row["operational_cost"],
            row["fuel_efficiency"],
            row["total_revenue"],
            row["roi_percent"],
        ])
    return response
