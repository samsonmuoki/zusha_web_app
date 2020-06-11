from django.contrib import admin


from .models import SaccoUser


class SaccoUserAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'sacco', 'first_name', 'last_name', 'email', 'phone',
        'username', 'password'
    )
    list_filter = ['sacco']
    search_fields = ['username', 'sacco', 'first_name', 'last_name']


admin.site.register(SaccoUser, SaccoUserAdmin)
