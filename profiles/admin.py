from django.contrib import admin
from .models import Profile, SupportRequest, ProfileChangeLog, LikeDislike


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'name', 'surnames', 'nick_name', 'department', 'role', 'profile_confirmed', 'role_confirmed'
    )
    list_editable = ('profile_confirmed', 'role_confirmed')
    list_filter = ('department', 'role', 'profile_confirmed', 'role_confirmed')
    search_fields = ('user__username', 'name', 'surnames', 'email', 'nick_name')
    readonly_fields = ('last_activity', 'is_online', 'slug')

    fieldsets = (
        (None, {
            'fields': (
            'user', 'name', 'surnames', 'email', 'photo', 'bio', 'department', 'role', 'nick_name', 'birthdate')
        }),
        ('Подтверждения', {
            'fields': ('profile_confirmed', 'role_confirmed')
        }),
        ('Статистика', {
            'fields': ('likes', 'dislikes')
        }),
        ('Дополнительная информация', {
            'fields': ('last_activity', 'slug', 'is_online')
        }),
    )

    def is_online(self, obj):
        return obj.is_online

    is_online.boolean = True
    is_online.short_description = 'Статус Онлайн'
    save_on_top = True
    save_as = True

@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'message', 'created_at')
    search_fields = ('email', 'message')
    readonly_fields = ('created_at',)


@admin.register(ProfileChangeLog)
class ProfileChangeLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'change_type', 'old_value', 'new_value', 'timestamp']
    search_fields = ('user__username', 'change_type', 'old_value', 'new_value')
    readonly_fields = ('timestamp',)


@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile', 'is_like')
    search_fields = ('user__username', 'profile__user__username')
    list_filter = ('is_like',)
