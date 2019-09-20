from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Register your models here.

admin.site.site_header = 'SHOP BURGER'
admin.site.index_title = 'Administración'
admin.site.site_title = 'SHOP BURGER'

#admin.site.unregister(User)
#admin.site.unregister(Group)