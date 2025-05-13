from django.contrib import admin
from .models import BlogContent


@admin.register(BlogContent)
class BlogContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    fields = ('title', 'image', 'content', 'video_url', 'video_file')