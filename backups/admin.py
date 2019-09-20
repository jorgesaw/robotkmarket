from django.contrib import admin

from .models import BackUp

# Register your models here.

class BackUpAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'created', 'desc' )
        }),
    )
    readonly_fields = ('created',)
    list_display = ('created', 'desc')
    ordering = ('-created',)
    search_fields = ('created',)
    date_hierarchy = 'created' # Jerarquizar por fechas
    list_filter = ('created', )

admin.site.register(BackUp, BackUpAdmin)
