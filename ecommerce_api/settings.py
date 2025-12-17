"""
Week 1: Django Settings for E-commerce Product API
---------------------------------------------------
This file contains all the configuration for our Django project.

Key configurations:
- Database: SQLite for development (Week 1), can be changed for production
- REST Framework: Authentication, permissions, filtering, and pagination
- Installed Apps: Django REST Framework and django-filter for API functionality
"""

import os
from pathlib import Path

# Build paths inside the project - BASE_DIR points to the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key secret in production!
# Week 4: This should be moved to environment variables for deployment
SECRET_KEY = 'your-secret-key-here-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Week 4: Update this for deployment
ALLOWED_HOSTS = ['*']


# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps for REST API functionality
    'rest_framework',      # Django REST Framework for building APIs
    'django_filters',      # Advanced filtering for API endpoints
    
    # Our custom apps
    'products',            # Main app for products and users
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_api.wsgi.application'


# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

# Week 1: Using SQLite for development - simple file-based database
# Week 4: Can be switched to PostgreSQL for production deployment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =============================================================================
# DJANGO REST FRAMEWORK CONFIGURATION
# =============================================================================

REST_FRAMEWORK = {
    # Week 3: Authentication classes - how users prove their identity
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',  # For browsable API
        'rest_framework.authentication.BasicAuthentication',    # For simple testing
    ],
    
    # Week 2: Permission classes - who can access what
    # IsAuthenticatedOrReadOnly: Anyone can read, only logged-in users can write
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    
    # Week 2: Filter backends for search and filtering
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    
    # Week 2: Pagination to limit results per page
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12  # Return 12 items per page
}


# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# =============================================================================
# STATIC FILES
# =============================================================================

STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'