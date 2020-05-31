from django.urls import path

from . import views


app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.get_all_reports_list, name='all_reports'),
    # path('all2/', views.get_reports2, name='reports2'),
    path(
        'vehicles', views.daily_summary_by_vehicles_reports,
        name='all_vehicles_reports_summary'
    ),
    path(
        'saccos', views.daily_summary_by_saccos_reports,
        name='all_saccos_reports_summary'
    ),
    path(
        'drivers', views.daily_summary_by_drivers_reports,
        name='all_drivers_reports_summary'
    ),
    path(
        'summary/<slug:regno>/<slug:date>/',
        views.fetch_reports_for_a_vehicle_on_a_specific_day,
        name='specific_day_vehicle_reports'
    ),
    path(
        'summary/<slug:sacco>/<slug:date>/',
        views.fetch_reports_for_a_sacco_on_a_specific_day,
        name='specific_day_sacco_reports'
    ),
    path(
        'summary/<slug:driver>/<slug:date>/',
        views.fetch_reports_for_a_driver_on_a_specific_day,
        name='specific_day_driver_reports'
    ),
    path(
        'vehicles/<slug:regno>/',
        views.fetch_all_reports_for_a_specific_vehicle,
        name='all_reports_for_a_specific_vehicle'
    ),
    path(
        'saccos/<slug:sacco>/',
        views.fetch_all_reports_for_a_specific_sacco,
        name='all_reports_for_a_specific_sacco'
    ),
    path(
        'drivers/<slug:driver>/',
        views.fetch_all_reports_for_a_specific_driver,
        name='all_reports_for_a_specific_driver'
    ),
    path(
        'vehicles/<slug:regno>/<int:report_id>/', views.get_speeding_instance,
        name='single_speeding_instance'
    ),
    path(
        'all/orderbysacco/', views.order_reports_by_sacco,
        name='order_reports_by_acco'
    ),
    path(
        'all/<slug:sacco>/<slug:regno>/',
        views.fetch_all_cases_for_a_specific_sacco_vehicle,
        name="vehicle_cases"
        # viewable by logged in sacco admin
    ),
    path(
        'all/<slug:sacco>/<slug:regno>/',
        views.fetch_all_cases_for_a_specific_sacco_driver,
        name="vehicle_cases"
        # viewable by logged in sacco admin
    ),

    path(
        'all/<slug:sacco>/<slug:regno>/<int:report_id>/<slug:status>',
        views.update_sacco_case_status,
        name='update_sacco_case'
        # viewable by logged in sacco admin
    ),
    path(
        'all/<slug:sacco>/<slug:regno>/<int:report_id>/',
        views.resolve_sacco_case,
        name='resolve_sacco_case'
        # viewable by a logged in sacco admin
    ),
    path('all/map/', views.view_all_reports_on_map, name='map'),
    # path('all/map2/', views.view_map2, name='map2'),

]
