from django.contrib import admin


from .models import (
    Sacco, Vehicle, Driver,
    SaccoDriver, SaccoVehicle
)


class SaccoAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'sacco_name', 'email', 'phone_number', 'license_status'
    )
    list_filter = ['sacco_name']
    search_fields = ['sacco_name']


class VehicleAdmin(admin.ModelAdmin):
    """."""
    list_display = ('registration_number', 'license_status')
    list_filter = ['license_status']
    search_fields = ['registration_number']


class DriverAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'driver_id', 'first_name', 'last_name', 'email',
        'phone_number', 'license_status'
    )
    list_filter = ['license_status']
    search_fields = [
        'driver_id', 'first_name', 'last_name', 'email', 'phone_number'
    ]


class SaccoVehicleAdmin(admin.ModelAdmin):
    """."""
    list_display = ['vehicle', 'sacco']
    list_filter = ['sacco']
    search_fields = ['vehicle', 'sacco']


class SaccoDriverAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'driver', 'sacco', 'first_name', 'last_name', 'email', 'phone_number'
    )
    list_filter = ['sacco']
    search_fields = [
        'sacco', 'first_name', 'last_name', 'email', 'phone_number'
    ]


admin.site.register(Sacco, SaccoAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(SaccoDriver, SaccoDriverAdmin)
admin.site.register(SaccoVehicle, SaccoVehicleAdmin)
