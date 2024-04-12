from django.contrib import admin

# Register your models here.
# oee_calculator/admin.py

from django.contrib import admin
from .models import Machine, ProductionLog

admin.site.register(Machine)
admin.site.register(ProductionLog)
# OEECalculator/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('oee_calculator.urls')),
]
