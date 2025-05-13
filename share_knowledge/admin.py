# share_knowledge/admin.py

from django.contrib import admin
from .models import Post, Comment

admin.site.register(Comment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

