from django.contrib import admin
from .models import FAQ, FAQCategory

# Register your models here.
@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_active', 'order', 'views', 'helpful_count']
    list_filter = ['is_active', 'category']
    search_fields = ['question', 'answer']
    list_editable = ['is_active', 'order']