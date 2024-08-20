from django.contrib import admin
from django.utils.html import format_html
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import News, NewsImage, LikeDislike, Comment
from django.utils import timezone


class NewsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm

    list_display = ('title', 'created_at', 'is_pinned', 'image_display', 'created_by')
    list_display_links = ('title',)
    search_fields = ('title', 'description')
    list_filter = ('is_pinned', 'created_at', 'created_by')
    date_hierarchy = 'created_at'
    ordering = ('-is_pinned', '-created_at')
    list_editable = ('is_pinned',)
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'is_pinned', 'created_by', 'created_at')
        }),
        ('Date Information', {
            'fields': ('updated_at',),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('updated_at', 'created_by')
    autocomplete_fields = ('created_by',)

    def image_display(self, obj):
        if obj.image and obj.image.image:
            return format_html('<img src="{}" style="height: 50px; width: auto;" />', obj.image.image.url)
        return 'No Image'

    image_display.short_description = 'Превью'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        if not obj.created_at:
            obj.created_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ('description', 'image_display')
    search_fields = ('description',)
    readonly_fields = ('image_display',)

    def image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px; width: auto;" />', obj.image.url)
        return 'No Image'

    image_display.short_description = 'Превью'


@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'vote', 'created_at')
    search_fields = ('user__username', 'news__title')
    list_filter = ('vote', 'created_at', 'news')
    autocomplete_fields = ('user', 'news')
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'content', 'created_at')
    search_fields = ('user__username', 'news__title', 'content')
    list_filter = ('created_at',)
    autocomplete_fields = ('user', 'news')
    list_per_page = 20
