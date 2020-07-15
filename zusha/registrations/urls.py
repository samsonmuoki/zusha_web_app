from django.urls import path

from . import views


app_name = 'registrations'

urlpatterns = [
    path('', views.index, name='index'),
    path('saccos/', views.get_all_saccos, name='saccos'),
    path(
        'saccos/dashboard/<slug:sacco_id>/',
        views.saccos_dashboard,
        name='saccos_dashboard'
    ),
    path(
        'saccos/dashboard/<slug:sacco_id>/pending_reports/',
        views.fetch_pending_reports_for_a_sacco,
        name="pending_reports_sacco"
    ),
    path(
        'saccos/dashboard/<slug:sacco_id>/in_progress_reports/',
        views.fetch_in_progress_reports_for_a_sacco,
        name="in_progress_reports_sacco"
    ),
    path(
        'saccos/dashboard/<slug:sacco_id>/resolved_reports/',
        views.fetch_resolved_reports_for_a_sacco,
        name="resolved_reports_sacco"
    ),
    path('saccos/signup', views.signup_sacco_admin, name='sacco_signup'),
    path('saccos/login', views.login_sacco_admin, name='sacco_login'),
    path('saccos/logout', views.logout_sacco_admin, name='sacco_logout'),
    path('drivers/', views.get_all_drivers, name='drivers'),
    path(
        'drivers/saccos/<slug:sacco_id>/',
        views.sacco_drivers_list,
        name='sacco_drivers_list'
    ),
    path('vehicles/', views.get_all_vehicles, name='vehicles'),

    path(
        'vehicles/<slug:registration_number>', views.get_a_single_vehicle,
        name='vehicle_details'
    ),
    path(
        'drivers/<int:driver_id>/', views.get_driver_details,
        name='driver_details'
    ),

    # DASHBOARD SACCO DRIVERS
    path(
        'saccos/dashboard/<slug:sacco_id>/drivers/',
        views.dashboard_sacco_drivers_list,
        name='dashboard_sacco_drivers_list'
    ),
    path(
        'saccos/dashboard/<slug:sacco_id>/drivers/add',
        views.add_driver,
        name='add_driver'
    ),
    path(
        'saccos/dashboard/<slug:sacco_id>/drivers/add/<slug:driver_id>/',
        views.confirm_driver,
        name="confirm_driver"
    ),
    path(
        'saccos/dashboard/<slug:sacco_id>/drivers/profile/<slug:driver_id>',
        views.sacco_driver_profile,
        name='sacco_driver_profile'
    ),

    # DASHBOARD SACCO VEHICLES
    path(
        'saccos/dashboard/<slug:sacco_id>/vehicles/',
        views.sacco_vehicles_list,
        name='dashboard_sacco_vehicles_list'
    ),
    path(
        'saccos/dashboard/<slug:sacco_id>/vehicles/add',
        views.add_vehicle,
        name='add_vehicle'
    ),
    path(
        'saccos/dashboard/<slug:sacco_id>/vehicles/add/<slug:regno>',
        views.confirm_vehicle,
        name="confirm_vehicle"
    ),
]
