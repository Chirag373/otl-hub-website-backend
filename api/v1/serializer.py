from rest_framework import serializers
from django.db import transaction
from core.models import User, Subscription
from api.models import BuyerProfile, RealtorProfile, SellerProfile, PartnerProfile
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class SignupSerializer(serializers.ModelSerializer):
    '''
    Serializer for user signup
    '''
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=User.UserRole.choices)
    license_number = serializers.CharField(required=False, allow_blank=True)
    company_brokerage = serializers.CharField(required=False, allow_blank=True)
    preferred_location = serializers.CharField(required=False, allow_blank=True)
    property_type = serializers.ChoiceField(choices=SellerProfile.PropertyType.choices, required=False, allow_blank=True)
    budget_range = serializers.ChoiceField(choices=BuyerProfile.BudgetRange.choices, required=False, allow_blank=True)
    years_of_experience = serializers.ChoiceField(choices=RealtorProfile.ExperienceLevel.choices, required=False)
    estimated_value = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    property_location = serializers.CharField(required=False, allow_blank=True)
    company_name = serializers.CharField(required=False, allow_blank=True)
    partnership_type = serializers.ChoiceField(choices=PartnerProfile.PartnershipType.choices, required=False)
    service_areas = serializers.CharField(required=False, allow_blank=True)
    website_url = serializers.URLField(required=False, allow_blank=True)
    business_license_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'role', 'license_number', 'company_brokerage', 'preferred_location', 'property_type', 'budget_range', 'years_of_experience', 'estimated_value', 'property_location', 'company_name', 'partnership_type', 'service_areas', 'website_url', 'business_license_number']


    def validate(self, data):
        role = data.get('role')

        if role == User.UserRole.BUYER:
            if not data.get('preferred_location'):
                raise serializers.ValidationError({"preferred_location": "Preferred location required for buyers."})
            if not data.get('budget_range'):
                raise serializers.ValidationError({"budget_range": "Budget range required for buyers."})

        elif role == User.UserRole.REALTOR:
            if not data.get('license_number'):
                raise serializers.ValidationError({"license_number": "License number required for realtors."})
            if not data.get('company_brokerage'):
                raise serializers.ValidationError({"company_brokerage": "Company brokerage required for realtors."})
            if data.get('years_of_experience') is None: 
                raise serializers.ValidationError({"years_of_experience": "Years of experience required for realtors."})

        elif role == User.UserRole.SELLER:
            if not data.get('property_type'):
                raise serializers.ValidationError({"property_type": "Property type required for sellers."})
            if data.get('estimated_value') is None:
                raise serializers.ValidationError({"estimated_value": "Estimated value required for sellers."})
            if not data.get('property_location'):
                raise serializers.ValidationError({"property_location": "Property location required for sellers."})

        elif role == User.UserRole.PARTNER:
            if not data.get('company_name'):
                raise serializers.ValidationError({"company_name": "Company name required for partners."})
            if not data.get('partnership_type'):
                raise serializers.ValidationError({"partnership_type": "Partnership type required for partners."})
            if not data.get('service_areas'):
                raise serializers.ValidationError({"service_areas": "Service areas required for partners."})
            if not data.get('website_url'):
                raise serializers.ValidationError({"website_url": "Website URL required for partners."})
            if not data.get('business_license_number'):
                raise serializers.ValidationError({"business_license_number": "Business license number required for partners."})

        return data

    @transaction.atomic
    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')

        # Pop all role-specific fields
        license_number = validated_data.pop('license_number', None)
        company_brokerage = validated_data.pop('company_brokerage', None)
        preferred_location = validated_data.pop('preferred_location', None)
        property_type = validated_data.pop('property_type', None)
        budget_range = validated_data.pop('budget_range', None)
        years_of_experience = validated_data.pop('years_of_experience', None)
        estimated_value = validated_data.pop('estimated_value', None)
        property_location = validated_data.pop('property_location', None)
        company_name = validated_data.pop('company_name', None)
        partnership_type = validated_data.pop('partnership_type', None)
        service_areas = validated_data.pop('service_areas', None)
        website_url = validated_data.pop('website_url', None)
        business_license_number = validated_data.pop('business_license_number', None)

        # Create user with password (create_user handles hashing)
        # Since USERNAME_FIELD = 'email', email is the first positional argument
        email = validated_data.pop('email')
        user = User(
            username=email,  # Django still needs username field set
            email=email,
            role=role,
            **validated_data
        )
        user.set_password(password)
        user.save()

        # Create profiles (validation ensures these values exist)
        if role == User.UserRole.BUYER:
            BuyerProfile.objects.create(
                user=user,
                preferred_location=preferred_location,
                budget_range=budget_range
            )
        elif role == User.UserRole.REALTOR:
            RealtorProfile.objects.create(
                user=user,
                license_number=license_number,
                company_brokerage=company_brokerage,
                years_of_experience=years_of_experience
            )
        elif role == User.UserRole.SELLER:
            SellerProfile.objects.create(
                user=user,
                property_type=property_type,
                estimated_value=estimated_value,
                property_location=property_location
            )
        elif role == User.UserRole.PARTNER:
            PartnerProfile.objects.create(
                user=user,
                company_name=company_name,
                partnership_type=partnership_type,
                service_areas=service_areas,
                website_url=website_url,
                business_license_number=business_license_number
            )

        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(_("Both email and password are required."))

        # authenticate() uses AUTHENTICATION_BACKENDS; works because USERNAME_FIELD = 'email'
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(_("Invalid email or password."))

        if not user.is_active:
            raise serializers.ValidationError(_("User account is disabled."))

        attrs['user'] = user
        return attrs
