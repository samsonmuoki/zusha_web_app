from django.urls import path

from . import views


app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('all1/', views.get_reports, name='reports'),
    path('all/', views.get_reports2, name='reports2'),
    path('all/<int:report_id>/', views.get_speeding_instance, name='speeding-instance'),
    path('all/map/', views.view_map, name='map'),
    # path('all/map2/', views.view_map2, name='map2'),
    # path('bysacco/', views.reports_by_sacco, name='reportsBySacco'),
    path('all/<slug:sacco>/', views.reports_by_sacco, name='reportsBySacco'),
    # path('vehicles/', views.view_all_vehicles, name="vehicles"),
]
