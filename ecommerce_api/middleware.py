"""
Custom middleware to exempt API endpoints from CSRF protection.
This allows API calls from the frontend without CSRF token issues.
"""

from django.utils.deprecation import MiddlewareMixin


class DisableCSRFForAPI(MiddlewareMixin):
    """
    Middleware to disable CSRF protection for API endpoints.
    API endpoints use token authentication, so CSRF is not needed.
    """
    
    def process_request(self, request):
        # Exempt all /api/ endpoints from CSRF
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None

