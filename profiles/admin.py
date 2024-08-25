from django.contrib import admin
from .models import *
from django.utils.html import format_html


@admin.register(RegRole)
class RegRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('name',)


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_tag', 'priority')
    list_editable = ('priority',)
    list_per_page = 20

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;"/>', obj.image.url)
        return 'Нет значка'

    image_tag.short_description = 'Значок'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'name', 'surnames', 'nick_name', 'department', 'role', 'profile_confirmed', 'role_confirmed', 'level',
        'rating',
    )
    list_editable = ('role_confirmed',)
    list_filter = ('department', 'role', 'profile_confirmed', 'role_confirmed')
    search_fields = ('user__username', 'name', 'surnames', 'email', 'nick_name')
    readonly_fields = ('last_activity', 'is_online', 'slug', 'level', 'rating')
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': (
                'user', 'name', 'surnames', 'email', 'photo', 'bio', 'reg_role', 'department', 'role', 'nick_name',
                'birthdate',
                'badges'
            )
        }),
        ('Подтверждения', {
            'fields': ('profile_confirmed', 'role_confirmed')
        }),
        ('Статистика', {
            'fields': ('likes', 'dislikes')
        }),
        ('Активность и Рейтинг', {
            'fields': ('rating', 'level', 'last_activity')
        }),
        ('Дополнительная информация', {
            'fields': ('slug', 'is_online')
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
    list_per_page = 20


@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile', 'is_like')
    search_fields = ('user__username', 'profile__user__username')
    list_filter = ('is_like',)
    list_per_page = 20


@admin.register(ProfileConfirmationToken)
class ProfileConfirmationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'is_expired')
    search_fields = ('user__username', 'token')
    list_filter = ('created_at',)

    def is_expired(self, obj):
        return obj.is_expired()

    is_expired.boolean = True
    is_expired.short_description = 'Истек'


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'subject', 'sent_at', 'user')
    search_fields = ('recipient', 'subject')
    list_filter = ('sent_at', 'user')
    list_per_page = 20


@admin.register(InvestigationRequest)
class InvestigationRequestAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'address', 'title', 'created_at', 'get_assigned_to', 'get_response_profile',
        'response_date', 'is_closed', 'get_closed_by'
    )
    list_filter = ('created_at', 'assigned_to', 'response_profile', 'closed_by', 'is_closed')
    search_fields = ('first_name', 'last_name', 'address', 'title', 'description', 'response')
    readonly_fields = ('created_at', 'completed_at', 'response_date', 'closed_by', 'is_closed')
    fieldsets = (
        (None, {
            'fields': (
                'first_name', 'last_name', 'address', 'passport_link', 'phone_number', 'title', 'description', 'image'
            )
        }),
        ('Дата и статус', {
            'fields': (
                'created_at', 'completed_at', 'response', 'response_profile', 'response_date', 'assigned_to',
                'closed_by', 'is_closed'
            ),
            'classes': ('collapse',),
        }),
    )
    ordering = ('-created_at',)

    def get_assigned_to(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.user.get_full_name()
        return 'Не назначено'

    get_assigned_to.short_description = 'Назначено профилю'

    def get_response_profile(self, obj):
        if obj.response_profile:
            return obj.response_profile.user.get_full_name()
        return 'Не указан'

    get_response_profile.short_description = 'Ответивший профиль'

    def get_closed_by(self, obj):
        if obj.closed_by:
            return obj.closed_by.user.get_full_name()
        return 'Не закрыто'

    get_closed_by.short_description = 'Закрыто профилем'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.response:
                return self.readonly_fields + ('assigned_to', 'closed_by')
            return self.readonly_fields
        return self.readonly_fields
