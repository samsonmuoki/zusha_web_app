from django.contrib import admin

# Register your models here.

from .models import (
    SpeedingInstance,
    DailyDriverReport,
    DailySaccoReport,
    DailyVehicleReport,
)


class SpeedingInstanceAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'regno', 'sacco', 'time', 'speed', 'driver', 'location'
    )
    list_filter = ['regno', 'sacco', 'driver']
    search_fields = ['regno', 'sacco', 'driver']


class DailVehicleReportAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'regno', 'sacco', 'date', 'count', 'ntsa_action', 'sacco_action'
    )
    list_filter = ['date', 'sacco']
    search_fields = ['regno', 'sacco']


class DailySaccoReportAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'sacco', 'date', 'count',
    )
    list_filter = ['date', 'sacco']
    search_fields = ['sacco']


class DailyDriverReportAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'driver', 'regno', 'sacco', 'date', 'count',
        'ntsa_action', 'ntsa_action_description'
    )
    list_filter = ['date', 'sacco']
    search_fields = ['driver', 'sacco']


admin.site.register(SpeedingInstance, SpeedingInstanceAdmin)
admin.site.register(DailyVehicleReport, DailVehicleReportAdmin)
admin.site.register(DailyDriverReport, DailyDriverReportAdmin)
admin.site.register(DailySaccoReport, DailySaccoReportAdmin)
