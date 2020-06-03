from django.contrib import admin

# Register your models here.

from .models import (
    Report,
    TrackDriverReports,
    TrackSaccoReports,
    TrackVehicleReports,
)


class ReportAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'regno', 'sacco', 'time', 'speed', 'driver', 'location'
    )
    list_filter = ['regno', 'sacco', 'driver']
    search_fields = ['regno', 'sacco', 'driver']


class TrackVehicleReportsAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'regno', 'sacco', 'date', 'count', 'ntsa_action', 'sacco_action'
    )
    list_filter = ['date', 'sacco']
    search_fields = ['regno', 'sacco']


class TrackSaccoReportsAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'sacco', 'date', 'count',
    )
    list_filter = ['date', 'sacco']
    search_fields = ['sacco']


class TrackDriverReportsAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'driver', 'sacco', 'date', 'count',
    )
    list_filter = ['date', 'sacco']
    search_fields = ['driver', 'sacco']


admin.site.register(Report, ReportAdmin)
admin.site.register(TrackVehicleReports, TrackVehicleReportsAdmin)
admin.site.register(TrackDriverReports, TrackDriverReportsAdmin)
admin.site.register(TrackSaccoReports, TrackSaccoReportsAdmin)
