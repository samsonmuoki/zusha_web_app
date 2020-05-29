from django.urls import path

from . import views


app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.get_reports, name='reports'),
    # path('all2/', views.get_reports2, name='reports2'),
    path(
        'summary', views.summary_vehicles_reports, name='summary'
    ),
    path(
        'summary/<slug:regno>/<slug:date>/',
        views.fetch_single_vehicle_reports,
        name='single_vehicle_reports'
    ),
    path(
        'all/<int:report_id>/', views.get_speeding_instance,
        name='speeding_instance'
    ),
    path('all/map/', views.view_all_reports_on_map, name='map'),
    # path('all/map2/', views.view_map2, name='map2'),
    path(
        'all/orderbysacco/', views.order_reports_by_sacco,
        name='order_reports_by_acco'
    ),
    path(
        'all/<slug:sacco>/', views.single_sacco_reports,
        name='singleSaccoReport'
    ),
    path(
        'all/<slug:sacco>/<slug:regno>/<int:report_id>/',
        views.resolve_sacco_case,
        name='resolve_sacco_case'
    ),
    path(
        'all/<slug:sacco>/<slug:regno>/<int:report_id>/<slug:status>',
        views.update_sacco_case_status,
        name='update_sacco_case'
    ),
    path(
        'all/<slug:sacco>/<slug:regno>/', views.single_vehicle_cases,
        name="vehicle_cases"
    ),
]
