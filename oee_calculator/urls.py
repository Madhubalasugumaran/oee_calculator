from django.urls import path
from . import views

urlpatterns = [
    path('oee_data/', views.oee_data, name='oee_data'),
    # other URL patterns
]