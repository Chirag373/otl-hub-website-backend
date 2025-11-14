#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to the path
sys.path.append("/Users/chirag/Desktop/project/otl-hub-website-backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "otlhubs.settings")
django.setup()

from core.models import User, Subscription
from api.models import BuyerProfile, RealtorProfile


def create_test_data():
    # Create a test realtor/agent
    try:
        realtor_user = User.objects.filter(role="REALTOR").first()
        if not realtor_user:
            realtor_user = User.objects.create_user(
                email="sarah.johnson@realty.com",
                password="testpass123",
                first_name="Sarah",
                last_name="Johnson",
                phone_number="(555) 987-6543",
                role="REALTOR",
            )
            RealtorProfile.objects.create(
                user=realtor_user,
                license_number="CA-DRE-12345678",
                company_brokerage="Premier Realty Group",
                years_of_experience="EXPERIENCED",
            )
        print(f"Realtor created/updated: {realtor_user.email}")
    except Exception as e:
        print(f"Error creating realtor: {e}")

    # Create a test buyer
    try:
        buyer_user = User.objects.filter(role="BUYER").first()
        if not buyer_user:
            buyer_user = User.objects.create_user(
                email="john.smith@email.com",
                password="testpass123",
                first_name="John",
                last_name="Smith",
                phone_number="(555) 123-4567",
                role="BUYER",
            )
            buyer_profile = BuyerProfile.objects.create(
                user=buyer_user,
                preferred_location="San Francisco, CA",
                budget_range="600000-800000",
            )
        else:
            buyer_profile = BuyerProfile.objects.get(user=buyer_user)

        # Always assign the realtor as agent
        buyer_profile.assigned_agent = realtor_user
        buyer_profile.save()

        print(f"Buyer created/updated: {buyer_user.email}")
        print(f"Assigned agent: {realtor_user.email}")
    except Exception as e:
        print(f"Error creating buyer: {e}")

    # Create a test subscription
    try:
        subscription = Subscription.objects.filter(user=buyer_user).first()
        if not subscription:
            subscription = Subscription.objects.create(
                user=buyer_user,
                subscription_type="BUYER_PRO",
                amount=99.00,
                payment_status="COMPLETED",
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now() + timedelta(days=335),
            )
        print(f"Subscription created/updated: {subscription.subscription_type}")
    except Exception as e:
        print(f"Error creating subscription: {e}")

    return buyer_user


if __name__ == "__main__":
    buyer = create_test_data()
    print(f"\nTest data created successfully!")
    print(f"Buyer email: {buyer.email}")
    print("You can now test the API with this buyer's credentials")
