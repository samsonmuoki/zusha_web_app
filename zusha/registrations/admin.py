from django.contrib import admin

# Register your models here.

from .models import Sacco, Vehicle, Driver

admin.site.register(Sacco)
admin.site.register(Vehicle)
admin.site.register(Driver)
