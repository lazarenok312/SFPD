from django.contrib import admin
from .models import *


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


@admin.register(ContractServiceStatus)
class ContractServiceStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')
    list_display_links = ('id',)
    list_editable = ('is_active',)
    actions = ['set_active', 'set_inactive']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if queryset.count() > 1:
            ContractServiceStatus.objects.exclude(id=queryset.first().id).delete()
        return queryset

    def has_add_permission(self, request):
        return ContractServiceStatus.objects.count() == 0

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if object_id is None and ContractServiceStatus.objects.exists():
            self.message_user(request, "Нельзя создать более одного объекта статуса службы контракта.", level='error')
            return redirect('admin:index')
        return super().changeform_view(request, object_id, form_url, extra_context)

    def set_active(self, request, queryset):
        queryset.update(is_active=True)
        for obj in queryset:
            obj.save()

    set_active.short_description = "Активировать выбранные службы"

    def set_inactive(self, request, queryset):
        queryset.update(is_active=False)
        for obj in queryset:
            obj.save()

    set_inactive.short_description = "Деактивировать выбранные службы"


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email',)


@admin.register(UnsubscribeToken)
class UnsubscribeTokenAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'created_at', 'is_valid')
    search_fields = ('email', 'token')
    list_filter = ('created_at',)
    readonly_fields = ('token', 'created_at')

    def is_valid(self, obj):
        return obj.is_valid()

    is_valid.boolean = True
    is_valid.short_description = "Действителен"


@admin.register(ChangeHistory)
class ChangeHistoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
