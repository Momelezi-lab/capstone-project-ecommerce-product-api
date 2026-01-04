"""
Week 1-3: Root URL Configuration for E-commerce Product API
-----------------------------------------------------------
This module defines the main URL routing for the entire project.

URL Structure:
- /admin/          -> Django admin panel
- /api/            -> All API endpoints (products, users, categories)
- /api/api-token-auth/  -> Week 3: Token authentication endpoint
- /api-auth/       -> DRF browsable API login/logout
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from products.views import index_view

urlpatterns = [
    # Frontend UI - serve at root
    path('', index_view, name='index'),
    
    # Django admin panel
    path('admin/', admin.site.urls),
    
    # All API endpoints from the products app
    path('api/', include('products.urls')),
    
    # Week 3: Token authentication endpoint
    # POST username and password to get an auth token
    path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    # DRF browsable API login/logout (for browser testing)
    path('api-auth/', include('rest_framework.urls')),
]
