from django.contrib import admin
from .models import News, NewsImage
from django.utils.html import format_html

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_pinned', 'image_display')
    search_fields = ('title', 'description')
    list_filter = ('is_pinned', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'is_pinned')
        }),
        ('Date Information', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def image_display(self, obj):
        if obj.image and obj.image.image:
            return format_html('<img src="{}" style="height: 50px; width: auto;" />', obj.image.image.url)
        return 'No Image'

    image_display.short_description = 'Image Preview'

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

    image_display.short_description = 'Image Preview'

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True
