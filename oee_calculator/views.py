
# views.py

from django.http import JsonResponse
from django.db.models import Sum
from .models import ProductionLog

def oee_data(request):
    production_logs = ProductionLog.objects.all()
    
    total_available_time = 24  # Total available time in hours (3 shifts of 8 hours each)
    
    # Calculate total operating time using Django aggregation
    total_operating_time = production_logs.aggregate(total_duration=Sum('duration'))['total_duration']
    
    if total_operating_time is None:
        total_operating_time = 0
    
    unplanned_downtime = total_available_time - total_operating_time

    total_products = production_logs.count()
    good_products = production_logs.filter(material_name='Good').count()
    bad_products = total_products - good_products

    availability = (total_available_time - unplanned_downtime) / total_available_time * 100 if total_available_time != 0 else 0
    performance = (total_available_time * total_products) / total_operating_time * 100 if total_operating_time != 0 else 0
    quality = (good_products / total_products) * 100 if total_products != 0 else 0

    oee = availability * performance * quality / 10000  # Convert to percentage

    # Gathered data
    available_time = 24  # Total available time in hours (e.g., 3 shifts of 8 hours each)
    unplanned_downtime = 2  # Total unplanned downtime in hours
    ideal_cycle_time = 5  # Ideal cycle time in minutes
    actual_output = 500  # Number of products produced
    good_products = 480  # Number of good products
    total_products = 500  # Total number of products produced

# Calculate Availability
    availability = ((available_time - unplanned_downtime) / available_time) * 100

# Calculate Performance
    available_operating_time = actual_output * (ideal_cycle_time / 60)  # Convert ideal cycle time to hours
    performance = (ideal_cycle_time * actual_output) / available_operating_time * 100

# Calculate Quality
    quality = (good_products / total_products) * 100

# Calculate OEE
    oee = (availability * performance * quality) / 10000  # Convert to percentage

    print("Availability: {:.2f}%".format(availability))
    print("Performance: {:.2f}%".format(performance))
    print("Quality: {:.2f}%".format(quality))
    print("OEE: {:.2f}%".format(oee))


    return JsonResponse({'Availability':availability,'Performance':performance,'Quality':quality,'oee':oee})
