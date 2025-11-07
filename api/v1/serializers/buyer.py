from rest_framework import serializers
from django.db import transaction
from core.models import BaseUserDetails, Role, BudgetRange
from django.contrib.auth.password_validation import validate_password
from api.models import BuyerProfile


class BuyerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    preferred_location = serializers.CharField(required=False, allow_blank=True, write_only=True)
    budget_range = serializers.ChoiceField(choices=BudgetRange.choices, required=True, write_only=True)

    class Meta:
        model = BaseUserDetails
        fields = [
            'first_name', 'last_name', 'email', 'password',
            'confirm_password', 'preferred_location', 'budget_range'
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_email(self, value):
        if BaseUserDetails.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def create(self, validated_data):
        with transaction.atomic():
            # Remove non-user fields
            budget_range = validated_data.pop('budget_range')
            preferred_location = validated_data.pop('preferred_location', '')
            property_type = validated_data.pop('property_type', '')
            validated_data.pop('confirm_password')
            
            user = BaseUserDetails.objects.create_user(
                username=validated_data['email'],
                role=Role.BUYER,
                **validated_data
            )       
            
            BuyerProfile.objects.create(
                user=user,
                budget_range=budget_range,
                preferred_locations=preferred_location,
                property_type=property_type
            )
            
            return user  # Return user instance, not dict


class BuyerListSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    preferred_location = serializers.SerializerMethodField()
    budget_range = serializers.SerializerMethodField()

    class Meta:
        model = BaseUserDetails
        fields = [
            'uuid', 'first_name', 'last_name', 'email', 'phone_number',
            'preferred_location', 'budget_range'
        ]

    def get_preferred_location(self, obj):
        try:
            return obj.buyer_profile.preferred_locations
        except BuyerProfile.DoesNotExist:
            return ""

    def get_budget_range(self, obj):
        try:
            return obj.buyer_profile.budget_range
        except BuyerProfile.DoesNotExist:
            return ""

class BuyerDashboardSerializer(serializers.ModelSerializer):
    preferred_location = serializers.SerializerMethodField()

    class Meta:
        model = BaseUserDetails
        fields = ['uuid', 'first_name', 'last_name', 'email',
            'preferred_location'
        ]

    def get_preferred_location(self, obj):
        try:
            return obj.buyer_profile.preferred_locations
        except:
            return ""