from django.contrib import admin
from .models import News, NewsImage, LikeDislike, Comment
from django.utils.html import format_html


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_pinned', 'image_display', 'created_by')
    search_fields = ('title', 'description')
    list_filter = ('is_pinned', 'created_at', 'created_by')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'is_pinned', 'created_at', 'created_by')
        }),
        ('Date Information', {
            'fields': ('updated_at',),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('updated_at', 'created_by')

    def image_display(self, obj):
        if obj.image and obj.image.image:
            return format_html('<img src="{}" style="height: 50px; width: auto;" />', obj.image.image.url)
        return 'No Image'

    image_display.short_description = 'Превью'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True


@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ('description', 'image_display')
    search_fields = ('description',)
    readonly_fields = ('image_display',)

    fieldsets = (
        (None, {
            'fields': ('description', 'image')
        }),
    )

    def image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px; width: auto;" />', obj.image.url)
        return 'No Image'

    image_display.short_description = 'Превью'

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True


@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'vote', 'created_at')
    search_fields = ('user__username', 'news__title')
    list_filter = ('vote', 'created_at')

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'content', 'created_at')
    search_fields = ('user__username', 'news__title', 'content')
    list_filter = ('created_at',)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True
