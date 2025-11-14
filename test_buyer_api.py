#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
from django.test import Client

# Add the project directory to the path
sys.path.append("/Users/chirag/Desktop/project/otl-hub-website-backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "otlhubs.settings")
django.setup()

from core.models import User, Subscription
from api.models import BuyerProfile, RealtorProfile
from rest_framework_simplejwt.tokens import RefreshToken


def setup_test_data():
    print("Setting up test data...")

    # Try to get existing data first
    try:
        buyer_user = User.objects.filter(role="BUYER").first()
        realtor_user = User.objects.filter(role="REALTOR").first()

        if buyer_user and realtor_user:
            print("✓ Using existing test data")
            # Ensure buyer has agent assigned
            buyer_profile = BuyerProfile.objects.get(user=buyer_user)
            buyer_profile.assigned_agent = realtor_user
            buyer_profile.save()

            # Ensure subscription exists
            subscription, created = Subscription.objects.get_or_create(
                user=buyer_user,
                defaults={
                    "subscription_type": "BUYER_PRO",
                    "amount": 99.00,
                    "payment_status": "COMPLETED",
                    "start_date": datetime.now() - timedelta(days=30),
                    "end_date": datetime.now() + timedelta(days=335),
                },
            )

            # Set password for authentication
            buyer_user.set_password("testpass123")
            buyer_user.save()

            print(f"  Buyer: {buyer_user.email}")
            print(f"  Agent: {realtor_user.email}")
            return buyer_user
    except:
        pass

    # Create new test data with unique identifiers
    import time

    timestamp = str(int(time.time()))

    # Create realtor
    realtor_user = User.objects.create_user(
        email=f"sarah.johnson{timestamp}@realty.com",
        password="testpass123",
        first_name="Sarah",
        last_name="Johnson",
        phone_number="(555) 987-6543",
        role="REALTOR",
    )

    RealtorProfile.objects.create(
        user=realtor_user,
        license_number=f"CA-DRE-{timestamp}",
        company_brokerage="Premier Realty Group",
        years_of_experience="EXPERIENCED",
    )

    # Create buyer
    buyer_user = User.objects.create_user(
        email=f"john.smith{timestamp}@email.com",
        password="testpass123",
        first_name="John",
        last_name="Smith",
        phone_number="(555) 123-4567",
        role="BUYER",
    )

    BuyerProfile.objects.create(
        user=buyer_user,
        preferred_location="San Francisco, CA",
        budget_range="600000-800000",
        assigned_agent=realtor_user,
    )

    # Create subscription
    Subscription.objects.create(
        user=buyer_user,
        subscription_type="BUYER_PRO",
        amount=99.00,
        payment_status="COMPLETED",
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now() + timedelta(days=335),
    )

    print(f"✓ New test data created successfully!")
    print(f"  Buyer: {buyer_user.email}")
    print(f"  Agent: {realtor_user.email}")

    return buyer_user


def test_api():
    # Setup test data
    buyer_user = setup_test_data()

    # Generate JWT token
    refresh = RefreshToken.for_user(buyer_user)
    access_token = str(refresh.access_token)

    print(f"\n🔐 Authentication successful")
    print(f"Access token generated for {buyer_user.email}")

    # Test the API endpoint using Django test client
    client = Client()
    headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

    print(f"\n📡 Making request to: /api/v1/buyer/profile/")
    try:
        response = client.get("/api/v1/buyer/profile/", **headers)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS - Buyer Profile Response:")
            print("=" * 50)
            import json

            print(json.dumps(data, indent=2))

            # Validate structure
            expected_fields = [
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "role",
                "member_since",
                "location",
                "budget_range",
                "agent",
                "subscription",
            ]

            actual_fields = list(data.keys())
            missing_fields = [f for f in expected_fields if f not in actual_fields]

            if missing_fields:
                print(f"\n❌ Missing fields: {missing_fields}")
            else:
                print(f"\n✅ All expected fields present: {expected_fields}")

            # Check nested objects
            if data.get("agent") and data["agent"] != {}:
                print("✅ Agent information included")
            else:
                print("⚠️ Agent information missing or empty")

            if data.get("subscription") and data["subscription"] != {}:
                print("✅ Subscription information included")
            else:
                print("⚠️ Subscription information missing or empty")

        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.content.decode()}")

    except Exception as e:
        print(f"❌ Request error: {e}")
        print("Make sure the Django server is running")


if __name__ == "__main__":
    test_api()
