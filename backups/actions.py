

def load_restore_data(model_admin, request, queryset):
    obj = queryset[0]
    print(obj)
    print()
    return True

load_restore_data.short_description = 'Restaurar datos'
