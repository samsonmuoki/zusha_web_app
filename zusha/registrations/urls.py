from django.urls import path

from . import views


app_name = 'registrations'

urlpatterns = [
    path('', views.index, name='index'),
    path('saccos/', views.get_all_saccos, name='saccos'),
    path(
        'saccos/dashboard/<slug:sacco>',
        views.saccos_dashboard,
        name='saccos_dashboard'
    ),
    path('saccos/signup', views.signup_sacco_admin, name='sacco_signup'),
    path('saccos/login', views.login_sacco_admin, name='sacco_login'),
    path('saccos/logout', views.logout_sacco_admin, name='sacco_logout'),
    path('drivers/', views.get_all_drivers, name='drivers'),
    path('drivers/add', views.add_driver, name='add_driver'),
    path('vehicles/', views.get_all_vehicles, name='vehicles'),
    path('vehicles/add', views.add_vehicle, name='add_vehicle'),
    path(
        'vehicles/<slug:registration_number>', views.get_a_single_vehicle,
        name='vehicle_details'
    ),
    path(
        'drivers/<int:driver_id>/', views.get_driver_details,
        name='driver_details'
    )
]
