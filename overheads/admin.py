from django.contrib import admin
from django.utils.html import format_html

from .models import Overhead, ItemOverhead
# Register your models here.
class ItemOverheadAdmin(admin.TabularInline):
    model = ItemOverhead
    fields = ('name', 'value')
    list_display = ('name', 'value')
    ordering = ('id',)
    list_editable = ('quantity', 'discount')
    extra = 1
    """
    def show_price(self, obj):
        return obj.actual_price
    show_price.short_description = 'Precio'
    """

class OverheadAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ( ('init_cash', 'date_overhead'), ('total', 'remaining_cash') )
        }),
    )
    readonly_fields = ('created', 'updated', 'total', 'remaining_cash')
    list_display = ('date_overhead', 'init_cash', 'color_html_total_display', 'color_html_remaining_cash_display')
    ordering = ('-date_overhead',)
    search_fields = ('date_overhead',)
    date_hierarchy = 'date_overhead' # Jerarquizar por fechas
    list_filter = ('date_overhead',)
    inlines = [ItemOverheadAdmin,]

    def color_html_total_display(self, obj):
        return format_html(
            f'<span style="color: red">{obj.total}</span>'
        )
    color_html_total_display.short_description = 'Total'

    def color_html_remaining_cash_display(self, obj):
        return format_html(
            f'<span style="color: green">{obj.total}</span>'
        )
    color_html_remaining_cash_display.short_description = 'Efectivo restante'
    

admin.site.register(Overhead, OverheadAdmin)
