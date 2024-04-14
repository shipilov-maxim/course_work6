from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'created_at', 'views_count')
