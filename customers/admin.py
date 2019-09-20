from django.contrib import admin

from utils.models_mixin import DontLogMixin
from .models import Customer
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    autocomplete_fields = ('city',)
    fields = ( 'id_card', ('first_name', 'last_name'), ('movile', 'telephone'), 'address', 'city' )
    readonly_fields = ('created', 'updated')
    list_display = ('full_name_display', 'movile', 'telephone', 'address', 'city')
    ordering = ('last_name', 'first_name', 'id_card')
    search_fields = ('id_card', 'last_name', 'first_name', 'address', 'city__name')
    date_hierarchy = 'updated' # Jerarquizar por fechas
    list_filter = ('last_name', 'address', 'city')

    def full_name_display(self, obj):
        return obj.full_name
    full_name_display.short_description = 'Nombre completo'

admin.site.register(Customer, CustomerAdmin)