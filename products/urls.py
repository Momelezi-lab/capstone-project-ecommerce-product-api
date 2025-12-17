"""
Week 2-3: URL Configuration for E-commerce Product API
-------------------------------------------------------
This module defines all the API routes using Django REST Framework's router.

I used DefaultRouter to automatically generate RESTful URL patterns for ViewSets.
The router creates standard CRUD endpoints following REST conventions.

Week 3 additions:
- /api/users/login/  - Token authentication login
- /api/users/logout/ - Token invalidation logout
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, 
    CategoryViewSet, 
    UserViewSet, 
    register_user,
    search_products,
    user_login,
    user_logout
)

# Week 2: Setting up the router to auto-generate CRUD endpoints
router = DefaultRouter()
router.register(r'products', ProductViewSet)    # /api/products/
router.register(r'categories', CategoryViewSet)  # /api/categories/
router.register(r'users', UserViewSet)           # /api/users/

urlpatterns = [
    # Custom endpoints BEFORE router URLs (order matters!)
    # These must come first to avoid being captured by router patterns
    
    # Week 2: User registration - public endpoint for new users to sign up
    path('users/register/', register_user, name='user-register'),
    
    # Week 3: Authentication endpoints
    path('users/login/', user_login, name='user-login'),      # Get auth token
    path('users/logout/', user_logout, name='user-logout'),   # Invalidate token
    
    # Week 2: Product search - dedicated search endpoint as per project requirements
    path('products/search/', search_products, name='product-search'),
    
    # Include all router-generated URLs
    path('', include(router.urls)),
]