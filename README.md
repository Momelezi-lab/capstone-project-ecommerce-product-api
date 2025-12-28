# E-commerce Product API

A RESTful API for managing products and users on an e-commerce platform, built with Django REST Framework.

## About This Project

This is my capstone project where I built a fully functional e-commerce API from scratch. The API supports complete CRUD operations for products and users, includes search functionality, and implements token-based authentication.

### What I Learned

- Building RESTful APIs with Django REST Framework
- Implementing token-based authentication and authorization
- Database modeling with Django ORM
- API filtering, searching, and pagination
- Writing clean, well-documented code
- Deploying Django applications

---

## Project Timeline

| Week   | Focus Area                                                | Status      |
| ------ | --------------------------------------------------------- | ----------- |
| Week 1 | Set up Django project, configure database & models        | ✅ Complete |
| Week 2 | Implement CRUD for products & users, add search endpoint  | ✅ Complete |
| Week 3 | Add token authentication, test API with Postman           | ✅ Complete |
| Week 4 | Deploy on Heroku, production configuration, final testing | ✅ Complete |

---

## Features

### Core Functionality

- **Product Management**: Full CRUD operations (Create, Read, Update, Delete)
- **User Management**: User registration, retrieval, update, and deletion
- **Search**: Search products by name or category
- **Categories**: Organize products into categories
- **Token Authentication**: Secure API access with token-based auth (Week 3)

### Technical Features

- Token-based authentication using Django REST Framework
- Pagination (12 items per page)
- Filtering by category, price, and stock
- Ordering by price, name, or creation date
- Input validation and error handling

---

## Tech Stack

- **Backend**: Python 3, Django 5.x
- **API Framework**: Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Token Authentication (DRF authtoken)
- **Filtering**: django-filter

---

## Database Schema

### User Model (Django Built-in)

| Field       | Type         | Description                |
| ----------- | ------------ | -------------------------- |
| id          | Integer (PK) | Auto-generated primary key |
| username    | CharField    | Unique username            |
| email       | EmailField   | User's email address       |
| password    | CharField    | Hashed password            |
| date_joined | DateTime     | Account creation timestamp |

### Product Model

| Field          | Type            | Description                  |
| -------------- | --------------- | ---------------------------- |
| id             | Integer (PK)    | Auto-generated primary key   |
| name           | CharField(200)  | Product name                 |
| description    | TextField       | Detailed description         |
| price          | DecimalField    | Price (up to 99,999,999.99)  |
| category       | ForeignKey      | Link to Category             |
| stock_quantity | PositiveInteger | Available inventory          |
| image_url      | URLField        | Optional product image URL   |
| created_by     | ForeignKey      | User who created the product |
| created_at     | DateTime        | Auto-set creation timestamp  |

### Category Model

| Field | Type           | Description                |
| ----- | -------------- | -------------------------- |
| id    | Integer (PK)   | Auto-generated primary key |
| name  | CharField(100) | Category name (unique)     |
| slug  | SlugField      | URL-friendly identifier    |

---

## API Endpoints

### Products

| Method | Endpoint                | Description          | Auth Required |
| ------ | ----------------------- | -------------------- | ------------- |
| GET    | `/api/products/`        | List all products    | No            |
| POST   | `/api/products/`        | Create a new product | Yes           |
| GET    | `/api/products/{id}/`   | Get product details  | No            |
| PUT    | `/api/products/{id}/`   | Update a product     | Yes           |
| PATCH  | `/api/products/{id}/`   | Partial update       | Yes           |
| DELETE | `/api/products/{id}/`   | Delete a product     | Yes           |
| GET    | `/api/products/search/` | Search products      | No            |

### Users & Authentication (Week 3)

| Method | Endpoint               | Description                       | Auth Required |
| ------ | ---------------------- | --------------------------------- | ------------- |
| POST   | `/api/users/register/` | Register new user (returns token) | No            |
| POST   | `/api/users/login/`    | Login and get auth token          | No            |
| POST   | `/api/users/logout/`   | Logout and invalidate token       | Yes           |
| GET    | `/api/users/`          | List all users                    | No            |
| GET    | `/api/users/{id}/`     | Get user details                  | No            |
| PUT    | `/api/users/{id}/`     | Update user                       | Yes           |
| DELETE | `/api/users/{id}/`     | Delete user                       | Yes           |

### Categories

| Method | Endpoint                | Description          | Auth Required |
| ------ | ----------------------- | -------------------- | ------------- |
| GET    | `/api/categories/`      | List all categories  | No            |
| GET    | `/api/categories/{id}/` | Get category details | No            |

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ecommerce-product-api.git
   cd ecommerce-product-api
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install django djangorestframework django-filter
   ```

4. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (for admin access)

   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the API**
   - Browsable API: http://127.0.0.1:8000/api/
   - Admin Panel: http://127.0.0.1:8000/admin/

---

## Authentication (Week 3)

This API uses **Token Authentication** as the primary authentication method. I implemented this in Week 3 to secure the API endpoints.

### How Token Authentication Works

1. User registers or logs in
2. Server returns an authentication token
3. Client includes token in all subsequent requests
4. Server validates token and processes request

### Getting a Token

**Option 1: Register a new user**

```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "email": "user@example.com", "password": "securepass123"}'
```

Response:

```json
{
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com",
    "date_joined": "2024-01-15T10:30:00Z"
  },
  "token": "your-auth-token-here",
  "message": "Registration successful! Use this token in the Authorization header."
}
```

**Option 2: Login with existing credentials**

```bash
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "existinguser", "password": "password123"}'
```

Response:

```json
{
  "token": "your-auth-token-here",
  "user_id": 1,
  "username": "existinguser",
  "email": "user@example.com",
  "message": "Login successful!"
}
```

### Using the Token

Include the token in the `Authorization` header of your requests:

```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Token your-auth-token-here" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Product", "description": "Description", "price": 99.99, "category_id": 1, "stock_quantity": 10}'
```

### Logging Out

To invalidate your token (logout):

```bash
curl -X POST http://127.0.0.1:8000/api/users/logout/ \
  -H "Authorization: Token your-auth-token-here"
```

Response:

```json
{
  "message": "Logout successful. Your token has been deleted."
}
```

After logout, you'll need to login again to get a new token.

---

## Usage Examples

### List All Products

```bash
curl http://127.0.0.1:8000/api/products/
```

### Create a Product (with Token Auth)

```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Token your-auth-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15",
    "description": "Latest Apple smartphone",
    "price": 999.99,
    "category_id": 1,
    "stock_quantity": 50
  }'
```

### Search Products

```bash
# Search by name
curl "http://127.0.0.1:8000/api/products/search/?name=iphone"

# Search by category
curl "http://127.0.0.1:8000/api/products/search/?category=electronics"

# Combined search
curl "http://127.0.0.1:8000/api/products/search/?name=phone&category=electronics"
```

### Filter and Order Products

```bash
# Filter by category slug
curl "http://127.0.0.1:8000/api/products/?category__slug=electronics"

# Order by price (ascending)
curl "http://127.0.0.1:8000/api/products/?ordering=price"

# Order by price (descending)
curl "http://127.0.0.1:8000/api/products/?ordering=-price"

# Use the built-in search
curl "http://127.0.0.1:8000/api/products/?search=laptop"
```

---

## Project Structure

```
ecommerce-product-api/
├── ecommerce_api/           # Main Django project settings
│   ├── __init__.py
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Root URL routing
│   ├── wsgi.py              # WSGI entry point
│   └── asgi.py              # ASGI entry point
│
├── products/                # Main application
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── admin.py             # Admin panel configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Database models (Product, Category)
│   ├── serializers.py       # API serializers
│   ├── urls.py              # App URL routing
│   ├── views.py             # API views and endpoints
│   └── tests.py             # Unit tests
│
├── db.sqlite3               # SQLite database (development)
├── manage.py                # Django management script
└── README.md                # This file
```

---

## Testing with Postman

I tested all API endpoints using Postman during Week 3. Here's how to set it up:

### Setup

1. Import the API endpoints into Postman
2. Set up an environment with:
   - `base_url`: `http://127.0.0.1:8000`
   - `token`: (your auth token after login)

### Authentication in Postman

1. First, call the login endpoint to get your token
2. Go to the **Authorization** tab
3. Select **API Key** from the Type dropdown
4. Set Key to `Authorization`
5. Set Value to `Token your-token-here`
6. Set "Add to" to `Header`

### Sample Postman Collection Endpoints

**Public Endpoints (no auth needed):**

- `GET {{base_url}}/api/products/` - List products
- `GET {{base_url}}/api/products/search/?name=test` - Search products
- `GET {{base_url}}/api/categories/` - List categories
- `POST {{base_url}}/api/users/register/` - Register user
- `POST {{base_url}}/api/users/login/` - Login

**Protected Endpoints (token required):**

- `POST {{base_url}}/api/products/` - Create product
- `PUT {{base_url}}/api/products/1/` - Update product
- `DELETE {{base_url}}/api/products/1/` - Delete product
- `POST {{base_url}}/api/users/logout/` - Logout

---

## Deployment (Week 4)

This API is deployed on Heroku and accessible at: **[Your Heroku URL Here]**

### Deployment Features:

- ✅ Production-ready configuration with environment variables
- ✅ PostgreSQL database (automatically provided by Heroku)
- ✅ Static files served via WhiteNoise
- ✅ Secure settings (DEBUG=False, environment-based secrets)
- ✅ Gunicorn web server for production

### Deployment Documentation:

- See `DEPLOYMENT_GUIDE.md` for step-by-step deployment instructions
- See `DEPLOYMENT_QUICK_REFERENCE.md` for quick command reference
- See `VIDEO_EXPLANATION_NOTES.md` for beginner-friendly explanation notes

---

## Future Enhancements

- [x] Token-based authentication (Week 3) ✅
- [x] Deployment to Heroku (Week 4) ✅
- [ ] Product image upload functionality
- [ ] Currency conversion API integration
- [ ] Order management system
- [ ] Shopping cart functionality
- [ ] Product reviews and ratings

---

## What I Would Do Differently

Looking back at this project, here are some things I learned and would consider for future projects:

1. **Start with a clear API design** - Planning all endpoints upfront helped avoid refactoring later
2. **Use environment variables early** - Set up python-decouple from day one for secrets management (implemented in Week 4)
3. **Write tests alongside features** - Test-driven development would catch bugs earlier
4. **Document as you go** - Comments and documentation are easier to write when the code is fresh
5. **Token refresh mechanism** - In a production app, I'd implement token refresh for better security
6. **Deployment is simpler than it seems** - Once you understand the process, deploying becomes straightforward

---

## Author

Built as a capstone project to demonstrate proficiency in Django REST Framework and API development.

---

## License

This project is for educational purposes as part of my learning journey.
