from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surnames', 'email', 'status', 'is_online')
    list_filter = ('user__is_staff', 'last_activity')
    search_fields = ('user__username', 'name', 'surnames', 'email')
    readonly_fields = ('slug', 'last_activity')

    def status(self, obj):
        return obj.status

    def is_online(self, obj):
        return obj.is_online

    status.short_description = 'Статус'
    is_online.short_description = 'Онлайн'

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'name', 'surnames', 'email', 'photo', 'slug', 'last_activity')
        }),
    )
