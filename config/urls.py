from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('accounts/', include('users.urls')),
    path('vehicles/', include('vehicles.urls')),
    path('drivers/', include('drivers.urls')),
    path('trips/', include('trips.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('fuel/', include('fuel.urls')),
    path('expenses/', include('expenses.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
