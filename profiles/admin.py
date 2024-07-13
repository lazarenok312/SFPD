from django.contrib import admin
from .models import Profile, SupportRequest


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surnames', 'email', 'department', 'role', 'profile_confirmed', 'role_confirmed', 'is_online')
    list_filter = ('department', 'role', 'profile_confirmed', 'role_confirmed')
    search_fields = ('user__username', 'name', 'surnames', 'email', 'nick_name')
    readonly_fields = ('last_activity', 'is_online', 'slug')

    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'surnames', 'email', 'photo', 'bio', 'department', 'role', 'nick_name')
        }),
        ('Confirmation', {
            'fields': ('profile_confirmed', 'role_confirmed')
        }),
        ('Additional Info', {
            'fields': ('last_activity', 'slug', 'is_online')
        }),
    )

    def is_online(self, obj):
        return obj.is_online
    is_online.boolean = True
    is_online.short_description = 'Online status'

    class SupportRequestAdmin(admin.ModelAdmin):
        list_display = ('email', 'message', 'created_at')
        search_fields = ('email', 'message')
        readonly_fields = ('created_at',)

    admin.site.register(SupportRequest, SupportRequestAdmin)
