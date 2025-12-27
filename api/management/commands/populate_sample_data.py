from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User
from api.models import SellerProfile, PropertyImage
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate database with sample property data for homepage latest properties'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample property data...')

        # Sample property data
        properties_data = [
            {
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'john.smith@example.com',
                'phone': '+1-555-0101',
                'address_number': '1234',
                'street_address': 'Maple Avenue',
                'city': 'Los Angeles',
                'state': 'CA',
                'zip_code': '90210',
                'county': 'Los Angeles',
                'property_type': 'SINGLE_FAMILY',
                'bedrooms': 4,
                'bathrooms': Decimal('2.5'),
                'sqft': 2500,
                'garage_spaces': 2,
                'estimated_value': Decimal('850000.00'),

                'description': 'Beautiful 4-bedroom home in prime Los Angeles location with modern amenities and spacious backyard.'
            },
            {
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'email': 'sarah.johnson@example.com',
                'phone': '+1-555-0102',
                'address_number': '567',
                'street_address': 'Oak Street',
                'city': 'San Francisco',
                'state': 'CA',
                'zip_code': '94102',
                'county': 'San Francisco',
                'property_type': 'CONDO',
                'bedrooms': 2,
                'bathrooms': Decimal('2.0'),
                'sqft': 1200,
                'garage_spaces': 1,
                'estimated_value': Decimal('1200000.00'),

                'description': 'Modern condo in the heart of San Francisco with stunning city views and premium finishes.'
            },
            {
                'first_name': 'Michael',
                'last_name': 'Davis',
                'email': 'michael.davis@example.com',
                'phone': '+1-555-0103',
                'address_number': '789',
                'street_address': 'Pine Road',
                'city': 'Austin',
                'state': 'TX',
                'zip_code': '78701',
                'county': 'Travis',
                'property_type': 'TOWNHOME',
                'bedrooms': 3,
                'bathrooms': Decimal('2.5'),
                'sqft': 1800,
                'garage_spaces': 2,
                'estimated_value': Decimal('450000.00'),

                'description': 'Charming townhome in vibrant Austin neighborhood, perfect for first-time buyers.'
            },
            {
                'first_name': 'Emily',
                'last_name': 'Wilson',
                'email': 'emily.wilson@example.com',
                'phone': '+1-555-0104',
                'address_number': '321',
                'street_address': 'Cedar Lane',
                'city': 'Seattle',
                'state': 'WA',
                'zip_code': '98101',
                'county': 'King',
                'property_type': 'SINGLE_FAMILY',
                'bedrooms': 5,
                'bathrooms': Decimal('3.0'),
                'sqft': 3200,
                'garage_spaces': 3,
                'estimated_value': Decimal('1100000.00'),

                'description': 'Spacious family home in Seattle with large lot and mountain views.'
            },
            {
                'first_name': 'David',
                'last_name': 'Brown',
                'email': 'david.brown@example.com',
                'phone': '+1-555-0105',
                'address_number': '654',
                'street_address': 'Elm Street',
                'city': 'Denver',
                'state': 'CO',
                'zip_code': '80202',
                'county': 'Denver',
                'property_type': 'SINGLE_FAMILY',
                'bedrooms': 3,
                'bathrooms': Decimal('2.0'),
                'sqft': 2000,
                'garage_spaces': 2,
                'estimated_value': Decimal('650000.00'),

                'description': 'Cozy mountain home in Denver with hiking trails nearby and modern updates.'
            },
            {
                'first_name': 'Lisa',
                'last_name': 'Garcia',
                'email': 'lisa.garcia@example.com',
                'phone': '+1-555-0106',
                'address_number': '987',
                'street_address': 'Birch Avenue',
                'city': 'Miami',
                'state': 'FL',
                'zip_code': '33101',
                'county': 'Miami-Dade',
                'property_type': 'CONDO',
                'bedrooms': 2,
                'bathrooms': Decimal('2.0'),
                'sqft': 1100,
                'garage_spaces': 1,
                'estimated_value': Decimal('550000.00'),

                'description': 'Beachfront condo in Miami with ocean views and resort-style amenities.'
            },
            {
                'first_name': 'Robert',
                'last_name': 'Miller',
                'email': 'robert.miller@example.com',
                'phone': '+1-555-0107',
                'address_number': '147',
                'street_address': 'Spruce Court',
                'city': 'Chicago',
                'state': 'IL',
                'zip_code': '60601',
                'county': 'Cook',
                'property_type': 'TOWNHOME',
                'bedrooms': 3,
                'bathrooms': Decimal('2.5'),
                'sqft': 1600,
                'garage_spaces': 1,
                'estimated_value': Decimal('425000.00'),

                'description': 'Historic townhome in Chicago with character and modern conveniences.'
            },
            {
                'first_name': 'Jennifer',
                'last_name': 'Taylor',
                'email': 'jennifer.taylor@example.com',
                'phone': '+1-555-0108',
                'address_number': '258',
                'street_address': 'Willow Drive',
                'city': 'Phoenix',
                'state': 'AZ',
                'zip_code': '85001',
                'county': 'Maricopa',
                'property_type': 'SINGLE_FAMILY',
                'bedrooms': 4,
                'bathrooms': Decimal('3.0'),
                'sqft': 2800,
                'garage_spaces': 3,
                'estimated_value': Decimal('720000.00'),

                'description': 'Desert oasis in Phoenix with pool, large yard, and energy-efficient features.'
            },
            {
                'first_name': 'James',
                'last_name': 'Anderson',
                'email': 'james.anderson@example.com',
                'phone': '+1-555-0109',
                'address_number': '369',
                'street_address': 'Palm Boulevard',
                'city': 'San Diego',
                'state': 'CA',
                'zip_code': '92101',
                'county': 'San Diego',
                'property_type': 'APARTMENT_UNIT',
                'bedrooms': 1,
                'bathrooms': Decimal('1.0'),
                'sqft': 800,
                'garage_spaces': 0,
                'estimated_value': Decimal('380000.00'),

                'description': 'Charming studio apartment in San Diego with ocean breezes and community amenities.'
            },
            {
                'first_name': 'Maria',
                'last_name': 'Rodriguez',
                'email': 'maria.rodriguez@example.com',
                'phone': '+1-555-0110',
                'address_number': '741',
                'street_address': 'Cypress Way',
                'city': 'Portland',
                'state': 'OR',
                'zip_code': '97201',
                'county': 'Multnomah',
                'property_type': 'SINGLE_FAMILY',
                'bedrooms': 3,
                'bathrooms': Decimal('2.0'),
                'sqft': 1900,
                'garage_spaces': 2,
                'estimated_value': Decimal('580000.00'),

                'description': 'Cozy cottage in Portland with garden, perfect for urban homesteaders.'
            },
            {
                'first_name': 'Christopher',
                'last_name': 'Martinez',
                'email': 'christopher.martinez@example.com',
                'phone': '+1-555-0111',
                'address_number': '852',
                'street_address': 'Magnolia Lane',
                'city': 'Nashville',
                'state': 'TN',
                'zip_code': '37201',
                'county': 'Davidson',
                'property_type': 'TOWNHOME',
                'bedrooms': 3,
                'bathrooms': Decimal('2.5'),
                'sqft': 1700,
                'garage_spaces': 2,
                'estimated_value': Decimal('495000.00'),

                'description': 'Modern townhome in Nashville music district with premium soundproofing.'
            },
            {
                'first_name': 'Amanda',
                'last_name': 'Lee',
                'email': 'amanda.lee@example.com',
                'phone': '+1-555-0112',
                'address_number': '963',
                'street_address': 'Juniper Street',
                'city': 'Boston',
                'state': 'MA',
                'zip_code': '02101',
                'county': 'Suffolk',
                'property_type': 'CONDO',
                'bedrooms': 2,
                'bathrooms': Decimal('1.5'),
                'sqft': 1000,
                'garage_spaces': 0,
                'estimated_value': Decimal('750000.00'),

                'description': 'Historic brownstone condo in Boston with original details and modern updates.'
            }
        ]

        created_properties = []

        for i, prop_data in enumerate(properties_data, 1):
            # Create user
            user = User.objects.create_user(
                email=prop_data['email'],
                password='password123',
                first_name=prop_data['first_name'],
                last_name=prop_data['last_name'],
                phone_number=prop_data['phone'],
                role=User.UserRole.SELLER
            )

            # Create seller profile
            seller_profile = SellerProfile.objects.create(
                user=user,
                address_number=prop_data['address_number'],
                street_address=prop_data['street_address'],
                city=prop_data['city'],
                state=prop_data['state'],
                zip_code=prop_data['zip_code'],
                county=prop_data['county'],
                property_type=prop_data['property_type'],
                property_description=prop_data['description'],
                estimated_value=prop_data['estimated_value'],
                bedrooms=prop_data['bedrooms'],
                bathrooms=prop_data['bathrooms'],
                sqft=prop_data['sqft'],
                garage_spaces=prop_data['garage_spaces'],

                has_active_listing=True,
                listing_created_at=timezone.now()
            )

            created_properties.append(seller_profile)
            self.stdout.write(f'Created property {i}: {seller_profile.property_description[:50]}...')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(created_properties)} sample properties for homepage!'
            )
        )
