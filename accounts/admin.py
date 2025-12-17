from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Attendance

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'membership_status', 'is_active']
    list_filter = ['role', 'membership_status', 'is_active', 'gender']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    ordering = ['-date_joined']
    
    fieldsets = (
        ('Basic Info', {'fields': ('email', 'password', 'first_name', 'last_name', 'phone')}),
        ('Personal Info', {'fields': ('date_of_birth', 'gender', 'profile_image', 'bio')}),
        ('Address', {'fields': ('street_address', 'city', 'state', 'zip_code', 'country')}),
        ('Emergency Contact', {'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')}),
        ('Membership', {'fields': ('role', 'membership_status', 'membership_plan', 'membership_start_date', 'membership_end_date')}),
        ('Medical Info', {'fields': ('medical_conditions', 'medications', 'allergies', 'injuries')}),
        ('Fitness', {'fields': ('fitness_goals',)}),
        ('Activity', {'fields': ('last_check_in', 'total_check_ins')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['member', 'check_in_time', 'check_out_time', 'duration_minutes', 'gym_class']
    list_filter = ['check_in_time', 'gym_class']
    search_fields = ['member__email', 'member__first_name', 'member__last_name']
    date_hierarchy = 'check_in_time'
