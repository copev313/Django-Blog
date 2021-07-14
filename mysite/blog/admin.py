from django.contrib import admin
from .models import Post, Comment

# Post Model:
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


# Comment Model:
@admin.action(description="Mark selected comments as active")
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)     

@admin.action(description="Mark selected comments as deactivated")
def make_deactivated(modeladmin, request, queryset):
    queryset.update(active=False)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    actions = [make_active, make_deactivated]
