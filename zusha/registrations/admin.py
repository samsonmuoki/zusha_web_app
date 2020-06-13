from django.contrib import admin


from .models import (
    Sacco, Vehicle, RegisteredDriver,
    SaccoDriver, SaccoVehicle
)


class SaccoAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'sacco_name', 'email', 'phone_number', 'date_registered',
        'last_inspection_date', 'license_status'
    )
    list_filter = ['sacco_name']
    search_fields = ['sacco_name']


class VehicleAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'registration_number', 'vehicle_body_type', 'inspection_status',
        'name_of_owner', 'owner_national_id', 'year_of_manufacture',
        'engine_capacity', 'registered_logbook_number'
    )
    list_filter = ['vehicle_body_type', 'inspection_status']
    search_fields = [
        'registration_number', 'name_of_owner', 'owner_national_id',
        'registered_logbook_number'
    ]


class RegisteredDriverAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'national_id', 'surname', 'other_names', 'sex', 'license_number',
        'license_status', 'county_of_residence', 'email', 'phone_number',
    )
    list_filter = ['license_status']
    search_fields = [
        'national_id', 'first_name', 'last_name', 'email', 'phone_number'
    ]


class SaccoVehicleAdmin(admin.ModelAdmin):
    """."""
    list_display = ['vehicle', 'sacco']
    list_filter = ['sacco']
    search_fields = ['vehicle', 'sacco']


class SaccoDriverAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        # 'driver', 'sacco', 'first_name', 'last_name', 'email', 'phone_number'
        # 'driver', 'sacco',
        'name', 'sacco',
    )
    list_filter = ['sacco']
    search_fields = [
        # 'sacco', 'first_name', 'last_name', 'email', 'phone_number'
        'sacco',
    ]


admin.site.register(Sacco, SaccoAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(RegisteredDriver, RegisteredDriverAdmin)
admin.site.register(SaccoDriver, SaccoDriverAdmin)
admin.site.register(SaccoVehicle, SaccoVehicleAdmin)
