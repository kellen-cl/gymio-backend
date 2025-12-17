from django.contrib import admin
from .models import Booking, ClassReview

# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'gym_class', 'class_date', 'status', 'checked_in', 'booking_date']
    list_filter = ['status', 'checked_in', 'class_date']
    search_fields = ['user__email', 'user__first_name', 'gym_class__name']
    date_hierarchy = 'class_date'

@admin.register(ClassReview)
class ClassReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'gym_class', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__email', 'gym_class__name', 'title', 'comment']
