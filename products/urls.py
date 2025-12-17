"""
Week 2: URL Configuration for E-commerce Product API
-----------------------------------------------------
This module defines all the API routes using Django REST Framework's router.

I used DefaultRouter to automatically generate RESTful URL patterns for ViewSets.
The router creates standard CRUD endpoints following REST conventions.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, 
    CategoryViewSet, 
    UserViewSet, 
    register_user,
    search_products
)

# Week 2: Setting up the router to auto-generate CRUD endpoints
router = DefaultRouter()
router.register(r'products', ProductViewSet)    # /api/products/
router.register(r'categories', CategoryViewSet)  # /api/categories/
router.register(r'users', UserViewSet)           # /api/users/

urlpatterns = [
    # Week 2: Custom endpoints BEFORE router URLs (order matters!)
    # These must come first to avoid being captured by router patterns
    
    # User registration - public endpoint for new users to sign up
    path('users/register/', register_user, name='user-register'),
    
    # Product search - dedicated search endpoint as per project requirements
    path('products/search/', search_products, name='product-search'),
    
    # Include all router-generated URLs
    path('', include(router.urls)),
]