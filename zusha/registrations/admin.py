from django.contrib import admin

# Register your models here.

from .models import (
    Sacco, Vehicle, Driver,
    SaccoDriver, SaccoVehicle
)

admin.site.register(Sacco)
admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(SaccoDriver)
admin.site.register(SaccoVehicle)
