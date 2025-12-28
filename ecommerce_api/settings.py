"""
Week 1-4: Django Settings for E-commerce Product API
-----------------------------------------------------
This file contains all the configuration for our Django project.

Key configurations:
- Database: SQLite for development (Week 1), PostgreSQL for production (Week 4)
- REST Framework: Authentication, permissions, filtering, and pagination
- Installed Apps: Django REST Framework and django-filter for API functionality
- Token Authentication: Added in Week 3 for secure API access
- Environment Variables: Added in Week 4 for secure production deployment
"""

import os
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project - BASE_DIR points to the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# SECURITY SETTINGS (Week 4: Using Environment Variables)
# =============================================================================

# SECURITY WARNING: keep the secret key secret in production!
# Week 4: Now using environment variables for security
# In production, set SECRET_KEY in your hosting platform's environment variables
SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
# Week 4: DEBUG should be False in production for security
# Set DEBUG=False in environment variables when deploying
DEBUG = config('DEBUG', default=True, cast=bool)

# Week 4: ALLOWED_HOSTS - list of domains that can access your API
# In production, replace with your actual domain (e.g., 'your-app.herokuapp.com')
# For development, we allow all hosts
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())


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
    'rest_framework',              # Django REST Framework for building APIs
    'rest_framework.authtoken',    # Week 3: Token authentication support
    'django_filters',              # Advanced filtering for API endpoints
    
    # Our custom apps
    'products',                    # Main app for products and users
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Week 4: Serve static files in production
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
# Week 4: Automatically switches to PostgreSQL in production (Heroku provides DATABASE_URL)
# If DATABASE_URL is set (like on Heroku), use PostgreSQL. Otherwise, use SQLite for local development.

import dj_database_url

# Check if we're in production (DATABASE_URL is set by Heroku)
if config('DATABASE_URL', default=None):
    # Production: Use PostgreSQL database from environment variable
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Development: Use SQLite database (local file)
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
    # Token authentication is the primary method for API clients
    # Session auth kept for the browsable API interface
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',    # Week 3: Token auth for API clients
        'rest_framework.authentication.SessionAuthentication',  # For browsable API in browser
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
# STATIC FILES (Week 4: Production Configuration)
# =============================================================================

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Week 4: Where collectstatic puts all static files

# Week 4: WhiteNoise configuration for serving static files in production
# WhiteNoise allows Django to serve static files directly (no need for separate web server)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'