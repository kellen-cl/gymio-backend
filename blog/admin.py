# blog/admin.py
from django.contrib import admin
from .models import BlogPost, BlogCategory, BlogComment

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'views', 'published_at']
    list_filter = ['status', 'is_featured', 'category', 'published_at']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    list_editable = ['status', 'is_featured']

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['user__email', 'post__title', 'content']
    list_editable = ['is_approved']