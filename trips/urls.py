from django.urls import path
from . import views

app_name = "trips"

urlpatterns = [
    path("", views.trip_list, name="list"),
    path("add/", views.trip_create, name="add"),
    path("<int:pk>/dispatch/", views.trip_dispatch, name="dispatch"),
    path("<int:pk>/complete/", views.trip_complete, name="complete"),
    path("<int:pk>/cancel/", views.trip_cancel, name="cancel"),
]
