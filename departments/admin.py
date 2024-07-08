from django.contrib import admin
from .models import Department, Role, ImportantInfo, PersonalFile, HonorsBoard

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name',)

@admin.register(ImportantInfo)
class ImportantInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'date_posted')
    list_filter = ('department',)
    search_fields = ('title', 'content')

@admin.register(PersonalFile)
class PersonalFileAdmin(admin.ModelAdmin):
    list_display = ('employee', 'details')
    search_fields = ('employee__user__username', 'details')

@admin.register(HonorsBoard)
class HonorsBoardAdmin(admin.ModelAdmin):
    list_display = ('employee', 'description', 'date_awarded')
    list_filter = ('date_awarded',)
    search_fields = ('employee__user__username', 'description')
