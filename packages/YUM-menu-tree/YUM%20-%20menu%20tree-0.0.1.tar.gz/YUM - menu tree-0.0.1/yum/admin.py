from django.contrib import admin
from .models import MenuItem
# Register your models here.

class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'name')

admin.site.register(MenuItem, MenuAdmin)
