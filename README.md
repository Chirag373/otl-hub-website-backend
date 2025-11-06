# OTL Hub Website Backend

Django REST Framework backend for OTL Hub with role-based user management system.

## Project Structure

```
otl-hub-website-backend/
├── otlhubs/                    # Main project configuration
│   ├── settings.py             # Django settings with DRF, JWT, CORS
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py & asgi.py       # WSGI/ASGI applications
│
├── core/                       # Common app
│   ├── models.py               # BaseModel, BaseUserDetails, Address, MembershipStatus
│   ├── admin.py                # Admin configuration for models
│   ├── utils.py                # Common helper functions
│   └── permissions.py          # Project-wide custom permissions
│
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
└── venv/                       # Virtual environment
```

## Features

- **Custom User Model**: `BaseUserDetails` with 5 roles (Admin, Buyer, Seller, Realtor, Partner)
- **Role-Based Access Control**: Role management with Django's permission system
- **JWT Authentication**: Token-based authentication using SimpleJWT
- **REST API**: Built with Django REST Framework
- **CORS Support**: Configured for frontend integration
- **Abstract Base Model**: `BaseModel` with created_at/updated_at timestamps

## Models

### BaseUserDetails (Custom User Model)
- Extends Django's AbstractUser
- Fields: role, first_name, last_name, email, phone_number, is_verified, is_updated
- 5 Roles: ADMIN, BUYER, SELLER, REALTOR, PARTNER

### Address
- User addresses with city, state, country, postal_code
- Support for multiple addresses per user
- Primary address flag

### MembershipStatus
- Partner membership tracking
- Fields: partner_since, partner_until, fee_paid, fee_amount

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd otl-hub-website-backend
```

### 2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser
```bash
python manage.py createsuperuser
```

### 6. Run development server
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/`

All models are registered with enhanced admin interfaces:
- BaseUserDetails: User management with role filtering
- Address: Address management with user search
- MembershipStatus: Membership tracking with payment status

## Dependencies

- **Django 4.2.7**: Web framework
- **djangorestframework 3.14.0**: REST API framework
- **djangorestframework-simplejwt 5.3.0**: JWT authentication
- **django-cors-headers 4.3.1**: CORS handling

## Configuration

### Custom User Model
The project uses a custom user model defined in `core.models.BaseUserDetails`. This is configured in `settings.py`:
```python
AUTH_USER_MODEL = 'core.BaseUserDetails'
```

### REST Framework Settings
- JWT Authentication enabled
- Pagination: 20 items per page
- Default permission: IsAuthenticated

### CORS Settings
Configured for local development:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Checking for Issues
```bash
python manage.py check
```

## API Structure (Ready for Implementation)

The project structure supports versioned API endpoints:
- `/api/v1/` - Version 1 API endpoints (to be implemented)

## License

[Your License Here]