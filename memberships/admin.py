from django.contrib import admin
from .models import MembershipPlan, MembershipSubscription

@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'duration_type', 'is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured', 'duration_type', 'access_hours']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'is_featured']

@admin.register(MembershipSubscription)
class MembershipSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'start_date', 'end_date', 'status', 'auto_renew']
    list_filter = ['status', 'auto_renew', 'start_date']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'plan__name']
    date_hierarchy = 'start_date'