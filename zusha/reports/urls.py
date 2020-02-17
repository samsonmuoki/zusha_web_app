from django.urls import path

from . import views


app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.get_reports, name='reports'),
    path('all/map/', views.view_map, name='map')
    # path('bysacco/', views.reports_by_sacco, name='reportsBySacco')
]
