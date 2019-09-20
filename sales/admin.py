from django.contrib import admin

from django.db.models import Count, Sum, Min, Max, DateTimeField
from django.db.models.functions import Trunc

from .models import Sale, ItemSale, SaleSummary
from .actions import fiscal_bill_emited, fiscal_bill_not_emited
# Register your models here.

class ItemSaleAdmin(admin.TabularInline):
    model = ItemSale
    autocomplete_fields = ('article_price',)
    fields = ('article_price', 'quantity', 'value')
    readonly_fields = ('value',)
    list_display = ('article_price', 'quantity', 'discount', 'value')
    ordering = ('id',)
    list_editable = ('quantity', 'discount')
    list_select_related = ('article',)
    extra = 5
    """
    def show_price(self, obj):
        return obj.actual_price
    show_price.short_description = 'Precio'
    """

class SaleAdmin(admin.ModelAdmin):
    #raw_id_fields = ('customer',)
    autocomplete_fields = ('customer',)
    fieldsets = (
        (None, {
            'fields': ( ('number_sale', 'date_sale', 'fiscal_bill'), ('customer', 'value') )
        }),
    )
    list_select_related = ('customer',)
    readonly_fields = ('created', 'updated', 'value')
    list_display = ('number_sale', 'date_sale', 'customer', 'fiscal_bill', 'value')
    ordering = ('-date_sale',)
    search_fields = ('number_sale', 'customer__id_card', 'customer__last_name', 'date_sale')
    date_hierarchy = 'date_sale' # Jerarquizar por fechas
    list_filter = ('date_sale', 'customer__id_card', 'customer__last_name')
    actions = [fiscal_bill_emited, fiscal_bill_not_emited]
    inlines = [ItemSaleAdmin,]

admin.site.register(Sale, SaleAdmin)

def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'
    if date_hierarchy + '__month' in request.GET:
        return 'day'
    if date_hierarchy + '__year' in request.GET:
        return 'week'
    return 'month'

@admin.register(SaleSummary)
class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/sale_summary_change_list.html'
    date_hierarchy = 'date_sale'
    list_filter = ('date_sale',)
    search_fields = ('date_sale',)
    actions = None
    # Prevent additional queries for pagination.
    show_full_result_count = False
    list_per_page = 50

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    #def has_change_permission(self, request, obj=None):
     #   return True

    #def has_module_permission(self, request):
     #   return True

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)


        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            # See issue #172.
            # When an invalid filter is used django will redirect. In this
            # case the response is an http redirect response and so it has
            # no context_data.
            return response

        # List view

        metrics = {
            'total': Count('id'),
            'total_sales': Sum('value'),
        }

        response.context_data['summary'] = list(
            qs
            .values('date_sale')
            .annotate(**metrics)
            .order_by('-date_sale')
        )

        from overheads.models import Overhead
        lista_gastos = Overhead.objects.values('date_overhead', 'total', 'init_cash').order_by('date_overhead')
        gastos = Overhead.objects.all().aggregate(Sum('total'))['total__sum']
        
        dic_gastos = {}
        dic_init_cash = {}
        
        for item in lista_gastos:
            dic_gastos[item['date_overhead']] = item['total'] # Convertimos a diccionario los datos de gastos
            dic_init_cash[item['date_overhead']] = item['init_cash']
        
        for item_venta in response.context_data['summary']:
            gasto = dic_gastos.get(item_venta['date_sale'], 0) # Buscamos el gasto del día
            inicio_caja = 0
            if gasto > 0:
                inicio_caja = dic_init_cash.get(item_venta['date_sale'], 0) # Buscamos el gasto del día
            item_venta['gasto'] = gasto
            item_venta['inicio_caja'] = inicio_caja
            item_venta['ganancia'] = item_venta['total_sales'] - gasto + inicio_caja

            # print('ITEM:', item_venta)
        # print(response.context_data['summary'][0])
        
        # List view summary
        if qs.count():
            response.context_data['summary_total'] = dict(qs.aggregate(**metrics))
            response.context_data['summary_total']['total_gastos'] = gastos
            response.context_data['summary_total']['neto'] = response.context_data['summary_total']['total_sales'] - gastos
        return response



