"""
Week 2-3: Views for E-commerce Product API
-------------------------------------------
This module contains all the ViewSets and API views for:
- Product CRUD operations (Create, Read, Update, Delete)
- Category listing (Read-only)
- User CRUD operations
- User registration endpoint (with auto token generation - Week 3)
- Product search functionality
- Token authentication login/logout (Week 3)

I used Django REST Framework's ViewSets to reduce boilerplate code
and provide consistent API behavior across all endpoints.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, UserSerializer


# =============================================================================
# PRODUCT VIEWS
# =============================================================================

class ProductViewSet(viewsets.ModelViewSet):
    """
    Week 2: Full CRUD for products with search, filter, and ordering support.
    
    Endpoints provided automatically by ModelViewSet:
    - GET    /api/products/          -> list all products (with pagination)
    - POST   /api/products/          -> create a new product (auth required)
    - GET    /api/products/{id}/     -> retrieve a single product
    - PUT    /api/products/{id}/     -> update a product (auth required)
    - PATCH  /api/products/{id}/     -> partial update (auth required)
    - DELETE /api/products/{id}/     -> delete a product (auth required)
    
    Search & Filter:
    - /api/products/?search=keyword  -> search by name, description, or category
    - /api/products/?category__slug=electronics -> filter by category
    - /api/products/?ordering=price  -> order by price (use -price for descending)
    """
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Week 2: Adding filter backends for search and ordering functionality
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'price', 'stock_quantity']
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'created_at', 'name']
    
    def perform_create(self, serializer):
        """
        Week 2: Override to automatically assign the logged-in user as product creator.
        This ensures every product has an owner without requiring it in the request body.
        """
        serializer.save(created_by=self.request.user)

# =============================================================================
# CATEGORY VIEWS
# =============================================================================

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Week 2: Read-only access to product categories.
    
    Endpoints provided by ReadOnlyModelViewSet:
    - GET /api/categories/       -> list all categories
    - GET /api/categories/{id}/  -> retrieve a single category
    
    Note: I used ReadOnlyModelViewSet because categories should be managed
    through the admin panel, not through the public API.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# =============================================================================
# USER VIEWS
# =============================================================================

class UserViewSet(viewsets.ModelViewSet):
    """
    Week 2: CRUD operations for user management.
    
    Endpoints:
    - GET    /api/users/          -> list all users
    - GET    /api/users/{id}/     -> retrieve user details
    - PUT    /api/users/{id}/     -> update user details (auth required)
    - DELETE /api/users/{id}/     -> delete user (auth required)
    
    Note: For new user registration, use the /api/users/register/ endpoint instead.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Week 2-3: Public endpoint for user self-registration.
    
    Endpoint: POST /api/users/register/
    
    Request body:
    {
        "username": "newuser",
        "email": "user@example.com",
        "password": "securepassword123"
    }
    
    Returns (Week 3 update - now includes token):
    - 201 Created: User successfully registered with auth token
    - 400 Bad Request: Validation errors (e.g., username taken)
    
    Week 3: I updated this to automatically create and return an auth token
    so users can immediately start making authenticated requests after registration.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Week 3: Create auth token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        # Return user data with token
        return Response({
            'user': serializer.data,
            'token': token.key,
            'message': 'Registration successful! Use this token in the Authorization header.'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =============================================================================
# AUTHENTICATION ENDPOINTS (Week 3)
# =============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    Week 3: Login endpoint that returns an authentication token.
    
    Endpoint: POST /api/users/login/
    
    Request body:
    {
        "username": "existinguser",
        "password": "userpassword123"
    }
    
    Returns:
    - 200 OK: Login successful with auth token and user info
    - 401 Unauthorized: Invalid credentials
    
    How to use the token:
    Include it in the Authorization header of subsequent requests:
    Authorization: Token <your-token-here>
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Validate that both fields are provided
    if not username or not password:
        return Response({
            'error': 'Please provide both username and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Authenticate the user
    user = authenticate(username=username, password=password)
    
    if user:
        # Get or create token for this user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'message': 'Login successful!'
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Invalid credentials. Please check username and password.'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    Week 3: Logout endpoint that deletes the user's auth token.
    
    Endpoint: POST /api/users/logout/
    
    Headers required:
    Authorization: Token <your-token-here>
    
    Returns:
    - 200 OK: Logout successful, token deleted
    
    Note: After logout, the user must login again to get a new token.
    This is more secure than keeping tokens alive indefinitely.
    """
    # Delete the user's token
    request.user.auth_token.delete()
    
    return Response({
        'message': 'Logout successful. Your token has been deleted.'
    }, status=status.HTTP_200_OK)


# =============================================================================
# SEARCH ENDPOINT
# =============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def search_products(request):
    """
    Week 2: Dedicated search endpoint for products by name or category.
    
    Endpoint: GET /api/products/search/
    
    Query Parameters:
    - name: Search term to match against product name (partial match)
    - category: Search term to match against category name (partial match)
    
    Examples:
    - /api/products/search/?name=laptop
    - /api/products/search/?category=electronics
    - /api/products/search/?name=phone&category=mobile
    
    Returns: List of matching products
    """
    # Get query parameters
    name_query = request.query_params.get('name', '')
    category_query = request.query_params.get('category', '')
    
    # Start with all products
    products = Product.objects.all()
    
    # Apply filters using Q objects for flexible querying
    if name_query:
        products = products.filter(Q(name__icontains=name_query))
    
    if category_query:
        products = products.filter(Q(category__name__icontains=category_query))
    
    # Order results by relevance (newest first)
    products = products.order_by('-created_at')
    
    # Serialize and return results
    serializer = ProductSerializer(products, many=True)
    return Response({
        'count': products.count(),
        'results': serializer.data
    })