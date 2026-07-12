import os
import django
import random
from datetime import date, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from vehicles.models import Vehicle
from drivers.models import Driver
from trips.models import Trip
from fuel.models import FuelLog
from maintenance.models import MaintenanceLog
from expenses.models import Expense

User = get_user_model()

def clear_db():
    print("Clearing database...")
    # Delete related logs first
    Expense.objects.all().delete()
    MaintenanceLog.objects.all().delete()
    FuelLog.objects.all().delete()
    Trip.objects.all().delete()
    Driver.objects.all().delete()
    Vehicle.objects.all().delete()
    # Delete users except root
    User.objects.exclude(username='root').delete()
    print("Database cleared.")

def create_users():
    print("Creating users...")
    users = [
        {"username": "john_manager", "role": User.Role.FLEET_MANAGER, "first_name": "John", "last_name": "Doe", "email": "john@transitops.com"},
        {"username": "sarah_safety", "role": User.Role.SAFETY_OFFICER, "first_name": "Sarah", "last_name": "Smith", "email": "sarah@transitops.com"},
        {"username": "alice_finance", "role": User.Role.FINANCIAL_ANALYST, "first_name": "Alice", "last_name": "Jones", "email": "alice@transitops.com"},
        {"username": "driver_bob", "role": User.Role.DRIVER, "first_name": "Bob", "last_name": "Miller", "email": "bob@transitops.com"},
        {"username": "driver_charlie", "role": User.Role.DRIVER, "first_name": "Charlie", "last_name": "Brown", "email": "charlie@transitops.com"},
    ]
    created = []
    for u in users:
        user = User.objects.create_user(
            username=u["username"],
            email=u["email"],
            password="password123",
            role=u["role"],
            first_name=u["first_name"],
            last_name=u["last_name"],
            phone=f"+1 555-010{random.randint(0, 9)}"
        )
        created.append(user)
    print(f"Created {len(created)} users.")
    return created

def create_vehicles():
    print("Creating vehicles...")
    vehicles_data = [
        {"registration_number": "NY-8492-AB", "name": "Ford Transit 350", "vehicle_type": Vehicle.VehicleType.VAN, "max_load_capacity_kg": 1500, "odometer_km": 45000, "acquisition_cost": 35000, "region": "Northeast"},
        {"registration_number": "CA-3829-XY", "name": "Volvo FH16", "vehicle_type": Vehicle.VehicleType.TRUCK, "max_load_capacity_kg": 18000, "odometer_km": 120000, "acquisition_cost": 145000, "region": "West"},
        {"registration_number": "TX-9012-CD", "name": "Mercedes Sprinter", "vehicle_type": Vehicle.VehicleType.VAN, "max_load_capacity_kg": 2000, "odometer_km": 82000, "acquisition_cost": 42000, "region": "South"},
        {"registration_number": "FL-5561-EF", "name": "Yamaha Cargo Bike", "vehicle_type": Vehicle.VehicleType.BIKE, "max_load_capacity_kg": 150, "odometer_km": 8500, "acquisition_cost": 4500, "region": "Southeast"},
        {"registration_number": "IL-2234-GH", "name": "Scania R500 Trailer", "vehicle_type": Vehicle.VehicleType.TRAILER, "max_load_capacity_kg": 24000, "odometer_km": 210000, "acquisition_cost": 160000, "region": "Midwest"},
        {"registration_number": "WA-4758-JK", "name": "Toyota Hilux", "vehicle_type": Vehicle.VehicleType.CAR, "max_load_capacity_kg": 800, "odometer_km": 55000, "acquisition_cost": 32000, "region": "Northwest"},
    ]
    created = []
    for v in vehicles_data:
        status = random.choice([Vehicle.Status.AVAILABLE, Vehicle.Status.AVAILABLE, Vehicle.Status.AVAILABLE, Vehicle.Status.ON_TRIP, Vehicle.Status.IN_SHOP])
        vehicle = Vehicle.objects.create(
            registration_number=v["registration_number"],
            name=v["name"],
            vehicle_type=v["vehicle_type"],
            max_load_capacity_kg=v["max_load_capacity_kg"],
            odometer_km=v["odometer_km"],
            acquisition_cost=v["acquisition_cost"],
            region=v["region"],
            status=status
        )
        created.append(vehicle)
    print(f"Created {len(created)} vehicles.")
    return created

def create_drivers():
    print("Creating drivers...")
    drivers_data = [
        {"name": "Robert Miller", "license_number": "DL-NY88392", "license_category": "Class A CDL", "contact_number": "+1 555-0111", "safety_score": 98.5},
        {"name": "Charlie Brown", "license_number": "DL-CA99401", "license_category": "Class B CDL", "contact_number": "+1 555-0122", "safety_score": 85.0},
        {"name": "David Miller", "license_number": "DL-TX44910", "license_category": "Class A CDL", "contact_number": "+1 555-0133", "safety_score": 92.2},
        {"name": "Emma Wilson", "license_number": "DL-FL88291", "license_category": "Class C", "contact_number": "+1 555-0144", "safety_score": 100.0},
        {"name": "Frank Thomas", "license_number": "DL-IL77492", "license_category": "Class A CDL", "contact_number": "+1 555-0155", "safety_score": 79.5},
    ]
    created = []
    for d in drivers_data:
        status = random.choice([Driver.Status.AVAILABLE, Driver.Status.AVAILABLE, Driver.Status.AVAILABLE, Driver.Status.ON_TRIP, Driver.Status.OFF_DUTY])
        license_expiry = date.today() + timedelta(days=random.randint(300, 1000))
        driver = Driver.objects.create(
            name=d["name"],
            license_number=d["license_number"],
            license_category=d["license_category"],
            license_expiry_date=license_expiry,
            contact_number=d["contact_number"],
            safety_score=d["safety_score"],
            status=status
        )
        created.append(driver)
    print(f"Created {len(created)} drivers.")
    return created

def create_trips_and_logs(users, vehicles, drivers):
    print("Creating trips, fuel, maintenance, and expenses...")
    sources = ["New York Depot", "Chicago Hub", "Los Angeles Center", "Miami Gateway", "Seattle Outpost", "Houston Facility"]
    destinations = ["Boston Terminal", "Detroit Port", "San Francisco Warehouse", "Atlanta Station", "Portland Yard", "Dallas Depot"]
    
    manager = User.objects.filter(role=User.Role.FLEET_MANAGER).first() or users[0]
    
    for i in range(15):
        vehicle = random.choice(vehicles)
        driver = random.choice(drivers)
        source = random.choice(sources)
        dest = random.choice([d for d in destinations if d != source])
        
        cargo_weight = random.randint(100, int(vehicle.max_load_capacity_kg))
        planned_distance = random.randint(50, 800)
        
        status_choice = random.choices(
            [Trip.Status.COMPLETED, Trip.Status.DISPATCHED, Trip.Status.DRAFT, Trip.Status.CANCELLED],
            weights=[0.6, 0.2, 0.1, 0.1],
            k=1
        )[0]
        
        created_dt = timezone.now() - timedelta(days=random.randint(1, 30), hours=random.randint(1, 23))
        dispatched_dt = created_dt + timedelta(hours=random.randint(1, 4)) if status_choice in [Trip.Status.DISPATCHED, Trip.Status.COMPLETED] else None
        completed_dt = dispatched_dt + timedelta(hours=int(planned_distance / 60)) if status_choice == Trip.Status.COMPLETED else None
        
        final_odom = vehicle.odometer_km + planned_distance + random.randint(-10, 10) if status_choice == Trip.Status.COMPLETED else None
        fuel = (planned_distance * random.uniform(0.1, 0.35)) if status_choice == Trip.Status.COMPLETED else None
        revenue = planned_distance * random.uniform(2.5, 5.0)
        
        trip = Trip.objects.create(
            source=source,
            destination=dest,
            vehicle=vehicle,
            driver=driver,
            cargo_weight_kg=cargo_weight,
            planned_distance_km=planned_distance,
            final_odometer_km=final_odom,
            fuel_consumed_liters=fuel,
            status=status_choice,
            revenue=revenue,
            created_by=manager,
            created_at=created_dt,
            dispatched_at=dispatched_dt,
            completed_at=completed_dt
        )
        
        if status_choice == Trip.Status.COMPLETED and fuel:
            FuelLog.objects.create(
                vehicle=vehicle,
                trip=trip,
                liters=fuel,
                cost=fuel * random.uniform(1.2, 1.6),
                date=completed_dt.date(),
                notes="Refuel after trip completion"
            )
            
        if status_choice in [Trip.Status.COMPLETED, Trip.Status.DISPATCHED]:
            if random.random() < 0.7:
                Expense.objects.create(
                    vehicle=vehicle,
                    category=Expense.Category.TOLL,
                    amount=random.uniform(10.0, 50.0),
                    date=dispatched_dt.date() if dispatched_dt else date.today(),
                    notes=f"Toll during trip {trip.id}"
                )
            if random.random() < 0.3:
                Expense.objects.create(
                    vehicle=vehicle,
                    category=Expense.Category.PARKING,
                    amount=random.uniform(15.0, 40.0),
                    date=dispatched_dt.date() if dispatched_dt else date.today(),
                    notes=f"Overnight parking"
                )
            if random.random() < 0.05:
                Expense.objects.create(
                    vehicle=vehicle,
                    category=Expense.Category.FINE,
                    amount=random.uniform(50.0, 200.0),
                    date=dispatched_dt.date() if dispatched_dt else date.today(),
                    notes="Speeding ticket"
                )

    for vehicle in vehicles:
        Expense.objects.create(
            vehicle=vehicle,
            category=Expense.Category.INSURANCE,
            amount=random.uniform(150.0, 300.0),
            date=date.today() - timedelta(days=random.randint(1, 20)),
            notes="Monthly fleet insurance premium"
        )
        
        for _ in range(random.randint(1, 3)):
            liters = random.uniform(30.0, 90.0)
            FuelLog.objects.create(
                vehicle=vehicle,
                liters=liters,
                cost=liters * random.uniform(1.2, 1.6),
                date=date.today() - timedelta(days=random.randint(1, 30)),
                notes="Routine refueling"
            )

        for _ in range(random.randint(1, 2)):
            status = random.choice([MaintenanceLog.Status.OPEN, MaintenanceLog.Status.CLOSED])
            reported_date = date.today() - timedelta(days=random.randint(5, 30))
            closed_date = reported_date + timedelta(days=random.randint(1, 4)) if status == MaintenanceLog.Status.CLOSED else None
            cost = random.uniform(80.0, 600.0) if status == MaintenanceLog.Status.CLOSED else 0
            
            titles = ["Oil Change & Filter", "Brake Pad Replacement", "Tire Rotation", "Engine Diagnostics", "AC Recharge"]
            title = random.choice(titles)
            
            MaintenanceLog.objects.create(
                vehicle=vehicle,
                title=title,
                description=f"Standard scheduled maintenance: {title}.",
                cost=cost,
                status=status,
                date_reported=reported_date,
                date_closed=closed_date
            )

if __name__ == "__main__":
    clear_db()
    users = create_users()
    vehicles = create_vehicles()
    drivers = create_drivers()
    create_trips_and_logs(users, vehicles, drivers)
    print("Database seeding completed successfully!")
