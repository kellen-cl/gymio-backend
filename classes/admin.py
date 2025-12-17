from django.contrib import admin
from .models import GymClass

@admin.register(GymClass)
class GymClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'instructor', 'category', 'day_of_week', 'start_time', 'capacity', 'is_active']
    list_filter = ['category', 'difficulty', 'day_of_week', 'is_active']
    search_fields = ['name', 'description', 'instructor__first_name', 'instructor__last_name']
    list_editable = ['is_active']
