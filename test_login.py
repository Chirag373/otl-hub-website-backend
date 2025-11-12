#!/usr/bin/env python
import os
import sys
import django
from django.test import Client
from django.contrib.auth import authenticate

# Add the project directory to the path
sys.path.append('/Users/chirag/Desktop/project/otl-hub-website-backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'otlhubs.settings')
django.setup()

from core.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def test_api():
    # Get a buyer user
    buyer = User.objects.filter(role='BUYER').first()
    if not buyer:
        print("No buyer user found")
        return

    print(f"Testing with buyer: {buyer.email}")

    # Authenticate user
    user = authenticate(email=buyer.email, password='testpass123')
    if not user:
        print("Authentication failed")
        return

    # Generate JWT token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    print(f"Authentication successful. Access token generated.")

    # Test the buyer profile endpoint using Django test client
    client = Client()
    response = client.get(
        '/api/v1/buyer/profile/',
        HTTP_AUTHORIZATION=f'Bearer {access_token}'
    )

    if response.status_code == 200:
        import json
        profile_data = response.json()
        print("\nBuyer Profile Response:")
        print("======================")
        print(json.dumps(profile_data, indent=2))

        # Check if the structure matches expected format
        expected_fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'member_since', 'location', 'budget_range', 'agent', 'subscription']
        actual_fields = list(profile_data.keys())

        print(f"\nExpected fields: {expected_fields}")
        print(f"Actual fields: {actual_fields}")

        missing_fields = [field for field in expected_fields if field not in actual_fields]
        if missing_fields:
            print(f"Missing fields: {missing_fields}")
        else:
            print("✓ All expected fields present!")

    else:
        print(f"Profile request failed: {response.status_code}")
        print(response.content.decode())

if __name__ == '__main__':
    test_api()
