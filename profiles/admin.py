from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import EmployeeProfile

User = get_user_model()

class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'role', 'get_full_name')
    list_filter = ('department', 'role')
    search_fields = ('user__username', 'department__name', 'role__name')

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Full Name'

admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
