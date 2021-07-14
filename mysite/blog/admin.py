from django.contrib import admin
from .models import Post


@admin.action(description="Mark selected blog posts as published")
def make_published(modeladmin, request, queryset):
    queryset.update(status='published')


@admin.action(description="Mark selected blog posts as drafts")
def make_draft(modeladmin, request, queryset):
    queryset.update(status='draft')
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title', )}
    raw_id_fields = ('author', )
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    actions = [make_published, make_draft]
    