from django.contrib import admin
from django.contrib import messages

from backups import models
from .models import BackUp
from .actions import load_restore_data
# Register your models here.

class BackUpAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'created', 'desc' )
        }),
    )
    readonly_fields = ('created',)
    list_display = ('created', 'desc', 'restore')
    ordering = ('-created',)
    search_fields = ('created',)
    date_hierarchy = 'created' # Jerarquizar por fechas
    list_filter = ('created', )
    actions = ['load_restore_data',]

    def load_restore_data(self, request, queryset):
        level = messages.INFO
        msg = models.MSG_RESTORE_DATA_DONE

        if queryset.count() > 1:
            msg = "Necesita seleccionar sólo un dato para restaurar."
            level=messages.WARNING
        elif not load_restore_data(self, request, queryset):
            msg = models.MSG_RESTORE_DATA_ERROR
            level=messages.ERROR

        return self.message_user(request, msg, level)
    load_restore_data.short_description = "Restaurar datos"

    def restore(self, obj):
        return 'RESTAURAR'
        link = reverse("admin:articles_category_change", args=[obj.category.id])
        return format_html('<a href="{}">{}</a>', link, obj.category.name)
        
    restore.short_description = "Datos"

admin.site.register(BackUp, BackUpAdmin)
