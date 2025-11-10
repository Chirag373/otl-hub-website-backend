# API JSON Examples

## 1. User Model

### User Registration (Request)

#### Buyer Registration
```json
{
  "email": "buyer@example.com",
  "username": "buyer123",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1-234-567-8900",
  "role": "BUYER"
}
```

#### Realtor Registration
```json
{
  "email": "realtor@example.com",
  "username": "realtor456",
  "password": "SecurePass123!",
  "first_name": "Jane",
  "last_name": "Smith",
  "phone_number": "+1-234-567-8901",
  "role": "REALTOR"
}
```

#### Seller Registration
```json
{
  "email": "seller@example.com",
  "username": "seller789",
  "password": "SecurePass123!",
  "first_name": "Mike",
  "last_name": "Johnson",
  "phone_number": "+1-234-567-8902",
  "role": "SELLER"
}
```

#### Partner Registration
```json
{
  "email": "partner@example.com",
  "username": "partner012",
  "password": "SecurePass123!",
  "first_name": "Sarah",
  "last_name": "Williams",
  "phone_number": "+1-234-567-8903",
  "role": "PARTNER"
}
```

### User Response (with profile)
```json
{
  "id": 1,
  "email": "buyer@example.com",
  "username": "buyer123",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1-234-567-8900",
  "role": "BUYER",
  "is_active": true,
  "is_staff": false,
  "date_joined": "2024-11-09T10:30:00Z",
  "created_at": "2024-11-09T10:30:00Z",
  "updated_at": "2024-11-09T10:30:00Z"
}
```

### User Login (Request)
```json
{
  "email": "buyer@example.com",
  "password": "SecurePass123!"
}
```

### User Login (Response with JWT)
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "buyer@example.com",
    "username": "buyer123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1-234-567-8900",
    "role": "BUYER",
    "created_at": "2024-11-09T10:30:00Z"
  }
}
```

---

## 2. Buyer Profile

### Create/Update Buyer Profile (Request)
```json
{
  "preferred_location": "Los Angeles, CA",
  "budget_range": "$500,000 - $750,000",
  "subscription_plan": "PRO",
  "subscription_start_date": "2024-11-09T10:30:00Z",
  "subscription_end_date": "2025-11-09T10:30:00Z"
}
```

### Buyer Profile Response
```json
{
  "id": 1,
  "user": 1,
  "preferred_location": "Los Angeles, CA",
  "budget_range": "$500,000 - $750,000",
  "subscription_plan": "PRO",
  "subscription_start_date": "2024-11-09T10:30:00Z",
  "subscription_end_date": "2025-11-09T10:30:00Z",
  "created_at": "2024-11-09T10:30:00Z",
  "updated_at": "2024-11-09T10:35:00Z"
}
```

### Complete Buyer with Profile Response
```json
{
  "id": 1,
  "email": "buyer@example.com",
  "username": "buyer123",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1-234-567-8900",
  "role": "BUYER",
  "created_at": "2024-11-09T10:30:00Z",
  "updated_at": "2024-11-09T10:30:00Z",
  "buyer_profile": {
    "id": 1,
    "preferred_location": "Los Angeles, CA",
    "budget_range": "$500,000 - $750,000",
    "subscription_plan": "PRO",
    "subscription_start_date": "2024-11-09T10:30:00Z",
    "subscription_end_date": "2025-11-09T10:30:00Z",
    "created_at": "2024-11-09T10:30:00Z",
    "updated_at": "2024-11-09T10:35:00Z"
  }
}
```

---

## 3. Realtor Profile

### Create/Update Realtor Profile (Request)
```json
{
  "license_number": "CA-DRE-12345678",
  "company_brokerage": "Premium Realty Group",
  "years_of_experience": "EXPERIENCED",
  "subscription_active": true,
  "subscription_start_date": "2024-11-09T10:30:00Z"
}
```

### Realtor Profile Response
```json
{
  "id": 1,
  "user": 2,
  "license_number": "CA-DRE-12345678",
  "company_brokerage": "Premium Realty Group",
  "years_of_experience": "EXPERIENCED",
  "years_of_experience_display": "6-10 years",
  "subscription_active": true,
  "subscription_start_date": "2024-11-09T10:30:00Z",
  "created_at": "2024-11-09T10:30:00Z",
  "updated_at": "2024-11-09T10:30:00Z"
}
```

### Complete Realtor with Profile Response
```json
{
  "id": 2,
  "email": "realtor@example.com",
  "username": "realtor456",
  "first_name": "Jane",
  "last_name": "Smith",
  "phone_number": "+1-234-567-8901",
  "role": "REALTOR",
  "created_at": "2024-11-09T10:30:00Z",
  "updated_at": "2024-11-09T10:30:00Z",
  "realtor_profile": {
    "id": 1,
    "license_number": "CA-DRE-12345678",
    "company_brokerage": "Premium Realty Group",
    "years_of_experience": "EXPERIENCED",
    "years_of_experience_display": "6-10 years",
    "subscription_active": true,
    "subscription_start_date": "2024-11-09T10:30:00Z",
    "created_at": "2024-11-09T10:30:00Z",
    "updated_at": "2024-11-09T10:30:00Z"
  }
}
```

---

## 4. Seller Profile

### Create/Update Seller Profile (Request)
```json
{
  "property_type": "RESIDENTIAL",
  "property_location": "San Francisco, CA",
  "estimated_value": "850000.00",
  "has_active_listing": true,
  "listing_created_at": "2024-11-09T10:30:00Z"
}
```

### Seller Profile Response
```json
{
  "id": 1,
  "user": 3,
  "property_type": "RESIDENTIAL",
  "property_type_display": "Residential",
  "property_location": "San Francisco, CA",
  "estimated_value": "850000.00",
  "has_active_listing": true,
  "listing_created_at": "2024-11-09T10:30:00Z",
  "created_at": "2024-11-09T10:30:00Z",
  "updated_at": "2024-11-09T10:30:00Z"
}
```

### Complete Seller with Profile Response
```json
{
  "id": 3,
  "email": "seller@example.com",
  "username": "seller789",
  "first_name": "Mike",
  "last_name": "Johnson",
  "phone_number": "+1-234-567-8902",
  "role": "SELLER",
  "created_at": "2024-11-09T10:30:00Z",
  "updated_at": "2024-11-09T10:30:00Z",
  "seller_profile": {
    "id": 1,
    "property_type": "RESIDENTIAL",
    "property_type_display": "Residential",
    "property_location": "San Francisco, CA",
    "estimated_value": "850000.00",
    "has_active_listing": true,
    "listing_created_at": "2024-11-09T10:30:00Z",
    "created_at": "2024-11-09T10:30:00Z",
    "updated_at": "2024-11-09T10:30:00Z"
  }
}
```

---

## 5. Partner Profile

### Create/Update Partner Profile (Request)
```json
{
  "company_name": "Premier Mortgage Solutions",
  "partnership_type": "MORTGAGE",
  "service_areas": "Los Angeles, San Diego, San Francisco, Sacramento",
  "subscription_active": true,
  "subscription_start_date": "2024-11-09T10:30:00Z"
}
```

### Partner Profile Response
```json
{
  "id": 1,
  "user": 4,
  "company_name": "Premier Mortgage Solutions",
  "partnership_type": "MORTGAGE",
  "partnership_type_display": "Mortgage Lender",
  "service_areas": "Los Angeles, San Diego, San Francisco, Sacramento",
  "subscription_active": true,
  "subscription_start_date": "2024-11-09T10:30:00Z",
  "created_at": "2024-11-09T10:30:00Z",
  "updated_at": "2024-11-09T10:30:00Z"
}
```

### Complete Partner with Profile Response
```json
{
  "id": 4,
  "email": "partner@example.com",
  "username": "partner012",
  "first_name": "Sarah",
  "last_name": "Williams",
  "phone_number": "+1-234-567-8903",
  "role": "PARTNER",
  "created_at": "2024-11-09T10:30:00Z",
  "updated_at": "2024-11-09T10:30:00Z",
  "partner_profile": {
    "id": 1,
    "company_name": "Premier Mortgage Solutions",
    "partnership_type": "MORTGAGE",
    "partnership_type_display": "Mortgage Lender",
    "service_areas": "Los Angeles, San Diego, San Francisco, Sacramento",
    "subscription_active": true,
    "subscription_start_date": "2024-11-09T10:30:00Z",
    "created_at": "2024-11-09T10:30:00Z",
    "updated_at": "2024-11-09T10:30:00Z"
  }
}
```

---

## 6. Subscription

### Create Subscription (Request)
```json
{
  "user": 1,
  "subscription_type": "BUYER_PRO",
  "amount": "49.99",
  "setup_fee": "10.00",
  "payment_status": "PENDING",
  "transaction_id": "",
  "start_date": "2024-11-09T10:30:00Z",
  "end_date": "2024-12-09T10:30:00Z"
}
```

### Subscription Response
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "email": "buyer@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "subscription_type": "BUYER_PRO",
  "subscription_type_display": "Buyer Pro Plan",
  "amount": "49.99",
  "setup_fee": "10.00",
  "total_amount": "59.99",
  "payment_status": "COMPLETED",
  "payment_status_display": "Completed",
  "transaction_id": "txn_1234567890",
  "start_date": "2024-11-09T10:30:00Z",
  "end_date": "2024-12-09T10:30:00Z",
  "created_at": "2024-11-09T10:30:00Z",
  "updated_at": "2024-11-09T10:32:00Z"
}
```

### User with Subscriptions List
```json
{
  "id": 1,
  "email": "buyer@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "BUYER",
  "subscriptions": [
    {
      "id": 1,
      "subscription_type": "BUYER_PRO",
      "amount": "49.99",
      "payment_status": "COMPLETED",
      "start_date": "2024-11-09T10:30:00Z",
      "end_date": "2024-12-09T10:30:00Z"
    },
    {
      "id": 2,
      "subscription_type": "BUYER_PRO",
      "amount": "49.99",
      "payment_status": "COMPLETED",
      "start_date": "2024-12-09T10:30:00Z",
      "end_date": "2025-01-09T10:30:00Z"
    }
  ]
}
```

---

## 7. List Endpoints

### List Users (Paginated)
```json
{
  "count": 50,
  "next": "http://api.example.com/api/v1/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "email": "buyer@example.com",
      "username": "buyer123",
      "first_name": "John",
      "last_name": "Doe",
      "role": "BUYER",
      "created_at": "2024-11-09T10:30:00Z"
    },
    {
      "id": 2,
      "email": "realtor@example.com",
      "username": "realtor456",
      "first_name": "Jane",
      "last_name": "Smith",
      "role": "REALTOR",
      "created_at": "2024-11-09T11:00:00Z"
    }
  ]
}
```

### List Realtors with Profiles
```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "email": "realtor@example.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "phone_number": "+1-234-567-8901",
      "realtor_profile": {
        "license_number": "CA-DRE-12345678",
        "company_brokerage": "Premium Realty Group",
        "years_of_experience": "EXPERIENCED",
        "subscription_active": true
      }
    }
  ]
}
```

---

## 8. Error Responses

### Validation Error
```json
{
  "errors": {
    "email": ["This field is required."],
    "phone_number": ["Enter a valid phone number."],
    "role": ["\"INVALID\" is not a valid choice."]
  }
}
```

### Authentication Error
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Permission Error
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Not Found Error
```json
{
  "detail": "Not found."
}
```

### Unique Constraint Error
```json
{
  "errors": {
    "email": ["User with this email already exists."],
    "license_number": ["Realtor profile with this license number already exists."]
  }
}
```

---

## 9. Filter and Search Examples

### Filter Users by Role
**Request:** `GET /api/v1/users/?role=BUYER`

**Response:**
```json
{
  "count": 20,
  "results": [
    {
      "id": 1,
      "email": "buyer@example.com",
      "role": "BUYER",
      "first_name": "John",
      "last_name": "Doe"
    }
  ]
}
```

### Search Realtors by Name or License
**Request:** `GET /api/v1/realtors/?search=Jane Smith`

**Response:**
```json
{
  "count": 1,
  "results": [
    {
      "id": 2,
      "email": "realtor@example.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "realtor_profile": {
        "license_number": "CA-DRE-12345678",
        "company_brokerage": "Premium Realty Group"
      }
    }
  ]
}
```

### Filter Subscriptions by Status
**Request:** `GET /api/v1/subscriptions/?payment_status=COMPLETED`

**Response:**
```json
{
  "count": 45,
  "results": [
    {
      "id": 1,
      "user": {
        "email": "buyer@example.com"
      },
      "subscription_type": "BUYER_PRO",
      "amount": "49.99",
      "payment_status": "COMPLETED",
      "start_date": "2024-11-09T10:30:00Z"
    }
  ]
}
```

---

## 10. Bulk Operations

### Create Multiple Subscriptions
**Request:** `POST /api/v1/subscriptions/bulk/`
```json
[
  {
    "user": 1,
    "subscription_type": "BUYER_PRO",
    "amount": "49.99",
    "start_date": "2024-11-09T10:30:00Z",
    "end_date": "2024-12-09T10:30:00Z"
  },
  {
    "user": 2,
    "subscription_type": "REALTOR_PROFESSIONAL",
    "amount": "99.99",
    "start_date": "2024-11-09T10:30:00Z",
    "end_date": "2024-12-09T10:30:00Z"
  }
]
```

**Response:**
```json
{
  "created": 2,
  "failed": 0,
  "results": [
    {
      "id": 1,
      "user": 1,
      "subscription_type": "BUYER_PRO",
      "payment_status": "PENDING"
    },
    {
      "id": 2,
      "user": 2,
      "subscription_type": "REALTOR_PROFESSIONAL",
      "payment_status": "PENDING"
    }
  ]
}
```

---

## Choice Field Values Reference

### User Roles
- `BUYER` - Buyer
- `REALTOR` - Realtor
- `SELLER` - Seller
- `PARTNER` - Partner

### Buyer Subscription Plans
- `BASIC` - Basic Plan
- `PRO` - Pro Plan

### Realtor Experience Levels
- `ENTRY` - 0-2 years
- `INTERMEDIATE` - 3-5 years
- `EXPERIENCED` - 6-10 years
- `EXPERT` - 10+ years

### Seller Property Types
- `RESIDENTIAL` - Residential
- `COMMERCIAL` - Commercial
- `LAND` - Land
- `MULTI_FAMILY` - Multi-Family

### Partner Partnership Types
- `MORTGAGE` - Mortgage Lender
- `INSURANCE` - Insurance Provider
- `INSPECTION` - Home Inspection
- `LEGAL` - Legal Services
- `CONTRACTOR` - Contractor
- `OTHER` - Other Services

### Subscription Types
- `BUYER_BASIC` - Buyer Basic Plan
- `BUYER_PRO` - Buyer Pro Plan
- `REALTOR_PROFESSIONAL` - Realtor Professional
- `SELLER_LISTING` - Seller Property Listing
- `PARTNER_BUSINESS` - Partner Business Subscription

### Payment Status
- `PENDING` - Pending
- `COMPLETED` - Completed
- `FAILED` - Failed
- `REFUNDED` - Refunded


