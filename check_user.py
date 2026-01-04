import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_api.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

user = User.objects.filter(username='demo_user').first()
if user:
    print(f"User exists: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is active: {user.is_active}")
    print(f"Is staff: {user.is_staff}")
    
    # Test authentication
    auth = authenticate(username='demo_user', password='demo123')
    if auth:
        print("[OK] Authentication successful!")
    else:
        print("[FAIL] Authentication failed!")
        print("Resetting the password...")
        user.set_password('demo123')
        user.save()
        print("[OK] Password reset to 'demo123'. Try logging in again.")
else:
    print("User 'demo_user' does not exist!")

