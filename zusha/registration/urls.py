from django.urls import path

from . import views


app_name = 'registration'

urlpatterns = [
    path('', views.index, name='index'),
    path('saccos/', views.get_all_saccos, name='saccos'),
    path('drivers/', views.get_all_drivers, name='drivers'),
    path('vehicles/', views.get_all_vehicles, name='vehicles'),
    path('vehicles/<slug:registration_number>', views.get_a_single_vehicle, name='vehicle_details'),
    path('drivers/<int:driver_id>/', views.get_driver_details, name='driver_details')
]
