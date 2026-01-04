"""
Vercel serverless function entry point for Django application.
This file allows Django to run on Vercel's serverless platform.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_api.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Initialize Django
application = get_wsgi_application()
