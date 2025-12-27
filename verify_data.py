#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'otlhubs.settings')
django.setup()

from core.models import User
from api.models import SellerProfile

def main():
    print("=== DATA VERIFICATION ===")

    # Check users
    seller_users = User.objects.filter(role='SELLER')
    print(f"Total SELLER users created: {seller_users.count()}")

    # Check properties
    properties = SellerProfile.objects.filter(has_active_listing=True)
    print(f"Total active properties: {properties.count()}")

    print("\n=== SAMPLE PROPERTIES ===")
    for i, prop in enumerate(properties[:12], 1):
        print(f"\n{i}. {prop.city}, {prop.state}")
        print(f"   Type: {prop.get_property_type_display()}")
        print(f"   Bedrooms: {prop.bedrooms}, Bathrooms: {prop.bathrooms}, SqFt: {prop.sqft}")
        print(f"   Value: ${prop.estimated_value:,.0f}")
        print(f"   Address: {prop.address_number} {prop.street_address}")
        print(f"   Seller: {prop.user.first_name} {prop.user.last_name}")

    print("\n=== VERIFICATION COMPLETE ===")

if __name__ == '__main__':
    main()
