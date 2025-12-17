"""
Week 1 & 2: Database Models for E-commerce Product API
-------------------------------------------------------
This module defines the database schema for the application.

Models:
- Category: Product categories for organizing inventory
- Product: Main product entity with all required fields

I chose to use Django's built-in User model for user management
instead of creating a custom User model, since the requirements
only need basic user fields (id, username, email, password, date_joined).
"""

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Week 1: Category model for organizing products.
    
    Each product belongs to one category, enabling:
    - Filtering products by category
    - Organizing the product catalog
    - SEO-friendly URLs via slug field
    
    Fields:
    - name: Display name for the category (e.g., "Electronics")
    - slug: URL-friendly version (e.g., "electronics")
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"  # Fix plural in admin panel

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Week 1: Product model - the main entity of our e-commerce API.
    
    This model stores all product information as specified in the requirements:
    - name: Product title displayed to customers
    - description: Detailed product information
    - price: Product price (Decimal for accuracy with currency)
    - category: Foreign key to Category for organization
    - stock_quantity: Available inventory count (replaces 'stock' from requirements)
    - image_url: Optional URL to product image (for future enhancement)
    - created_by: Links product to the user who created it
    - created_at: Auto-set timestamp when product is created
    
    Week 2: This model supports full CRUD operations through ProductViewSet.
    """
    # Basic product information
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Pricing - using Decimal for accurate currency calculations
    # max_digits=10, decimal_places=2 allows prices up to 99,999,999.99
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Category relationship - CASCADE means deleting a category deletes its products
    # related_name='products' allows category.products.all() queries
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    
    # Inventory tracking - PositiveIntegerField prevents negative stock
    stock_quantity = models.PositiveIntegerField()
    
    # Optional image URL - blank=True allows products without images
    image_url = models.URLField(max_length=500, blank=True)
    
    # Track who created the product - useful for multi-vendor scenarios
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Auto-set creation timestamp - auto_now_add sets this once on creation
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']  # Newest products first by default