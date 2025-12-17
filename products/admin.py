"""
Week 1 & 2: Django Admin Configuration
---------------------------------------
This module registers our models with Django's admin interface.

The admin panel allows us to:
- Manage categories and products through a web interface
- Test data creation without using the API
- Monitor and debug data during development
"""

from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Week 2: Admin configuration for Category model.
    
    list_display: Columns shown in the list view
    prepopulated_fields: Auto-generate slug from name
    """
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}  # Auto-fill slug as you type name
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Week 2: Admin configuration for Product model.
    
    Features:
    - List view shows key product info at a glance
    - Filter sidebar for quick category/stock filtering
    - Search across name and description
    - Organized form fields for easy editing
    """
    list_display = ['name', 'category', 'price', 'stock_quantity', 'created_by', 'created_at']
    list_filter = ['category', 'created_at']  # Filter sidebar
    search_fields = ['name', 'description']   # Search box
    readonly_fields = ['created_at']          # Can't edit timestamp
    
    # Organize form into logical sections
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'image_url')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'category', 'stock_quantity')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)  # Collapsible section
        }),
    )
