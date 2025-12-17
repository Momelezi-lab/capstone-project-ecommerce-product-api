from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, UserSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    Week 2: full CRUD for products + search/filter/order support.
    Using ModelViewSet to get list/retrieve/create/update/destroy.
    """
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'price', 'stock_quantity']
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'created_at']

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Week 2: allow public read-only access to categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    Week 2: basic CRUD for users with hashed passwords.
    Restricted to authenticated access for mutating actions.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Week 2: dedicated endpoint for user self-service registration.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)