from django.contrib import admin
from .models import ContactMessage, GymInfo

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'subject', 'created_at']
    search_fields = ['name', 'email', 'message']
    date_hierarchy = 'created_at'
    list_editable = ['status']

@admin.register(GymInfo)
class GymInfoAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'updated_at']