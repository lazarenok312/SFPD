from django.contrib import admin
from .models import Department, Role, ImportantInfo


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
