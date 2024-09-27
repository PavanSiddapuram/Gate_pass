from django.contrib import admin
from .models import UserProfile, GatePass, ActionLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'institution', 'sub_department')  # Display key fields for quick overview
    search_fields = ('user__username', 'role', 'institution', 'sub_department')  # Enable search functionality

@admin.register(GatePass)
class GatePassAdmin(admin.ModelAdmin):
    list_display = (
        'pass_id', 'date_time', 'employee_name', 'approved_by_department_head',
        'approved_by_security_head', 'return_status', 'expected_return_date'
    )  # Display key fields for gate pass data
    list_filter = ('approved_by_department_head', 'approved_by_security_head', 'return_status')  # Filters for admin
    search_fields = ('pass_id', 'employee_name', 'product_name')  # Search functionality

@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('gate_pass', 'action_by', 'action_type', 'action_date')  # Show key action log fields
    list_filter = ('action_type', 'action_date')  # Filters for quick access to specific actions
    search_fields = ('gate_pass__pass_id', 'action_by__username')  # Enable search based on gate pass or user
