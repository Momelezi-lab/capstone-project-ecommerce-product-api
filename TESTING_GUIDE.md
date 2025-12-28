# API Testing Guide

This guide will walk you through testing all the endpoints of the E-commerce Product API.

## Prerequisites

1. Make sure the Django server is running:
   ```bash
   python3 manage.py runserver
   ```

2. The server should be accessible at: `http://127.0.0.1:8000`

---

## Method 1: Testing with cURL (Command Line)

### Step 1: Test Public Endpoints (No Authentication)

#### List All Products
```bash
curl http://127.0.0.1:8000/api/products/
```

#### Get a Single Product
```bash
curl http://127.0.0.1:8000/api/products/1/
```

#### List All Categories
```bash
curl http://127.0.0.1:8000/api/categories/
```

#### Search Products by Name
```bash
curl "http://127.0.0.1:8000/api/products/search/?name=iphone"
```

#### Search Products by Category
```bash
curl "http://127.0.0.1:8000/api/products/search/?category=electronics"
```

---

### Step 2: User Registration

Register a new user (this will return a token automatically):

```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

**Expected Response:**
```json
{
  "user": {
    "id": 2,
    "username": "testuser",
    "email": "test@example.com",
    "date_joined": "2024-01-15T10:30:00Z"
  },
  "token": "abc123def456...",
  "message": "Registration successful! Use this token in the Authorization header."
}
```

**⚠️ IMPORTANT:** Copy the `token` value from the response - you'll need it for authenticated requests!

---

### Step 3: User Login (Alternative to Registration)

If you already have a user account, login to get a token:

```bash
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Expected Response:**
```json
{
  "token": "abc123def456...",
  "user_id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "message": "Login successful!"
}
```

**⚠️ Copy the token!**

---

### Step 4: Test Authenticated Endpoints

Replace `YOUR_TOKEN_HERE` with the actual token you received.

#### Create a Product
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "description": "This is a test product",
    "price": 99.99,
    "category_id": 1,
    "stock_quantity": 50
  }'
```

#### Update a Product
```bash
curl -X PUT http://127.0.0.1:8000/api/products/1/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Product Name",
    "description": "Updated description",
    "price": 149.99,
    "category_id": 1,
    "stock_quantity": 75
  }'
```

#### Delete a Product
```bash
curl -X DELETE http://127.0.0.1:8000/api/products/1/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

#### Logout (Invalidate Token)
```bash
curl -X POST http://127.0.0.1:8000/api/users/logout/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## Method 2: Testing with Postman

### Setup Postman

1. **Download Postman** (if you don't have it): https://www.postman.com/downloads/

2. **Create a New Environment**
   - Click the gear icon (⚙️) in the top right
   - Click "Add"
   - Name it "E-commerce API"
   - Add these variables:
     - `base_url` = `http://127.0.0.1:8000`
     - `token` = (leave empty for now, we'll set it after login)

3. **Select the environment** from the dropdown in the top right

---

### Step-by-Step Postman Testing

#### 1. Register a New User

- **Method:** POST
- **URL:** `{{base_url}}/api/users/register/`
- **Headers:**
  - `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "username": "postmantest",
    "email": "postman@test.com",
    "password": "postman123"
  }
  ```
- **Click Send**
- **Copy the token** from the response and paste it into your environment variable `token`

#### 2. Login (Alternative)

- **Method:** POST
- **URL:** `{{base_url}}/api/users/login/`
- **Headers:**
  - `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- **Click Send**
- **Copy the token** to your environment variable

#### 3. List All Products

- **Method:** GET
- **URL:** `{{base_url}}/api/products/`
- **No headers needed**
- **Click Send**

#### 4. Create a Product (Authenticated)

- **Method:** POST
- **URL:** `{{base_url}}/api/products/`
- **Headers:**
  - `Authorization: Token {{token}}`
  - `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "name": "Postman Test Product",
    "description": "Created via Postman",
    "price": 199.99,
    "category_id": 1,
    "stock_quantity": 100
  }
  ```
- **Click Send**

#### 5. Update a Product

- **Method:** PUT
- **URL:** `{{base_url}}/api/products/1/` (replace 1 with actual product ID)
- **Headers:**
  - `Authorization: Token {{token}}`
  - `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "name": "Updated via Postman",
    "description": "This was updated",
    "price": 249.99,
    "category_id": 1,
    "stock_quantity": 80
  }
  ```
- **Click Send**

#### 6. Delete a Product

- **Method:** DELETE
- **URL:** `{{base_url}}/api/products/1/` (replace 1 with actual product ID)
- **Headers:**
  - `Authorization: Token {{token}}`
- **Click Send**

#### 7. Search Products

- **Method:** GET
- **URL:** `{{base_url}}/api/products/search/?name=iphone`
- **Click Send**

#### 8. Logout

- **Method:** POST
- **URL:** `{{base_url}}/api/users/logout/`
- **Headers:**
  - `Authorization: Token {{token}}`
- **Click Send**

---

## Method 3: Testing with Browsable API (Browser)

The Django REST Framework provides a browsable API interface.

1. **Open your browser** and go to: `http://127.0.0.1:8000/api/`

2. **You'll see a list of available endpoints**

3. **To test authenticated endpoints:**
   - Click "Log in" in the top right
   - Enter your username and password
   - Now you can use the forms to create/update/delete products

4. **Test endpoints directly:**
   - Click on any endpoint (e.g., `/api/products/`)
   - Use the form at the bottom to make POST requests
   - Use the "OPTIONS" button to see available methods

---

## Quick Test Script

Here's a complete test sequence you can run in your terminal:

```bash
#!/bin/bash

BASE_URL="http://127.0.0.1:8000"

echo "=== 1. Testing Public Endpoints ==="
echo "Listing products..."
curl -s "$BASE_URL/api/products/" | python3 -m json.tool | head -20

echo -e "\n=== 2. Registering New User ==="
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/users/register/" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser'$(date +%s)'", "email": "test'$(date +%s)'@example.com", "password": "testpass123"}')

echo "$REGISTER_RESPONSE" | python3 -m json.tool

# Extract token (requires jq or manual copy)
TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")

echo -e "\n=== 3. Token received: $TOKEN ==="

echo -e "\n=== 4. Creating Product with Token ==="
curl -s -X POST "$BASE_URL/api/products/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "description": "Testing", "price": 99.99, "category_id": 1, "stock_quantity": 10}' \
  | python3 -m json.tool

echo -e "\n=== 5. Testing Search ==="
curl -s "$BASE_URL/api/products/search/?name=test" | python3 -m json.tool

echo -e "\n=== 6. Logging Out ==="
curl -s -X POST "$BASE_URL/api/users/logout/" \
  -H "Authorization: Token $TOKEN" \
  | python3 -m json.tool

echo -e "\n=== Tests Complete! ==="
```

Save this as `test_api.sh`, make it executable (`chmod +x test_api.sh`), and run it!

---

## Common Issues & Solutions

### Issue: "Invalid token"
**Solution:** Make sure you're using the correct token format:
- Header: `Authorization: Token your-token-here`
- Not: `Authorization: Bearer your-token-here`
- Not: `Authorization: your-token-here`

### Issue: "Authentication credentials were not provided"
**Solution:** You're trying to access a protected endpoint without authentication. Add the Authorization header with your token.

### Issue: "Invalid credentials"
**Solution:** Check your username and password. Make sure you're using the correct credentials for login.

### Issue: "Category with id=X does not exist"
**Solution:** First, check what categories exist:
```bash
curl http://127.0.0.1:8000/api/categories/
```
Then use a valid category_id when creating products.

---

## Testing Checklist

Use this checklist to ensure you've tested everything:

- [ ] List products (GET /api/products/)
- [ ] Get single product (GET /api/products/1/)
- [ ] List categories (GET /api/categories/)
- [ ] Search by name (GET /api/products/search/?name=...)
- [ ] Search by category (GET /api/products/search/?category=...)
- [ ] Register user (POST /api/users/register/)
- [ ] Login (POST /api/users/login/)
- [ ] Create product with token (POST /api/products/)
- [ ] Update product with token (PUT /api/products/1/)
- [ ] Delete product with token (DELETE /api/products/1/)
- [ ] Logout (POST /api/users/logout/)
- [ ] Verify token is invalid after logout

---

## Next Steps

Once you've tested everything locally, you're ready for Week 4: Deployment!

