"""
Week 2: Serializers for E-commerce Product API
-----------------------------------------------
This module handles conversion between Python objects and JSON.

Serializers serve two main purposes:
1. Convert model instances to JSON for API responses
2. Validate incoming JSON data and convert to model instances

I used ModelSerializer to automatically generate fields based on model definitions,
reducing boilerplate code while maintaining full control over field behavior.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Week 2: Serializer for Category model.
    
    Simple serializer that exposes all category fields.
    Used for both listing categories and as a nested serializer in products.
    """
    class Meta:
        model = Category
        fields = '__all__'  # Includes: id, name, slug


class UserSerializer(serializers.ModelSerializer):
    """
    Week 2: Serializer for Django's built-in User model.
    
    Key design decisions:
    - password is write_only: Never expose passwords in API responses
    - date_joined is read_only: Auto-set by Django, not user-editable
    - Custom create/update methods to properly hash passwords
    
    This matches the User Model schema from requirements:
    - id (PK) - auto-generated
    - username - required
    - email - required  
    - password - required (hashed before storage)
    - date_joined - auto-set
    """
    # write_only=True ensures password is never included in responses
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'date_joined']
        read_only_fields = ['id', 'date_joined']

    def create(self, validated_data):
        """
        Week 2: Custom create to ensure password is properly hashed.
        
        Django's set_password() method handles the hashing using
        the password hasher configured in settings (PBKDF2 by default).
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Week 2: Custom update to handle password changes safely.
        
        Only rehash password if a new one is provided.
        Other fields are updated normally.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Hash the new password
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    """
    Week 2: Serializer for Product model with nested category.
    
    Key design decisions:
    - category: Read-only nested serializer for rich response data
    - category_id: Write-only integer for creating/updating products
    - created_by: Read-only, automatically set in the view
    
    This approach means:
    - GET requests return full category details (name, slug)
    - POST/PUT requests only need category_id (integer)
    
    Example POST request body:
    {
        "name": "iPhone 15",
        "description": "Latest Apple smartphone",
        "price": 999.99,
        "category_id": 1,
        "stock_quantity": 50
    }
    
    Example GET response:
    {
        "id": 1,
        "name": "iPhone 15",
        "description": "Latest Apple smartphone",
        "price": "999.99",
        "category": {"id": 1, "name": "Electronics", "slug": "electronics"},
        "stock_quantity": 50,
        "created_by": "admin",
        "created_at": "2024-01-15T10:30:00Z"
    }
    """
    # Nested serializer for rich GET responses
    category = CategorySerializer(read_only=True)
    
    # Integer field for POST/PUT - references Category.id
    category_id = serializers.IntegerField(write_only=True)
    
    # Display username instead of user ID, set automatically in view
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'