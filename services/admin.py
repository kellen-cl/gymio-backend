# services/admin.py
from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'order']