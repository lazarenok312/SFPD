from django.contrib import admin
from .models import Department, Role, ImportantInfo, PoliceAcademyPosition, DepartmentStaff

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    search_fields = ('name', 'department__name')
    list_filter = ('department',)

@admin.register(ImportantInfo)
class ImportantInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'date_posted')
    search_fields = ('title', 'content', 'department__name')
    list_filter = ('department', 'date_posted')
    date_hierarchy = 'date_posted'

@admin.register(PoliceAcademyPosition)
class PoliceAcademyPositionAdmin(admin.ModelAdmin):
    list_display = ('position', 'nickname', 'description', 'photo')
    search_fields = ('nickname', 'position')
    list_filter = ('position',)

@admin.register(DepartmentStaff)
class DepartmentStaffAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'discord_url', 'vk_url', 'photo')
    search_fields = ('name', 'title')
    list_filter = ('title',)