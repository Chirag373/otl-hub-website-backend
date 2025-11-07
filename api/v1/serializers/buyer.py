from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from core.models import BaseUserDetails, BudgetRange, Role
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
    
    def create(self, validated_data):

        user = BaseUserDetails.objects.create_user(
            username=validated_data['email'], 
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            role=Role.BUYER
        )
        
        BuyerProfile.objects.create(
            user=user,
            budget_range=validated_data.get('budget_range'),
            preferred_locations=validated_data.get('preferred_location', '')
        )
        
        return user


class BuyerListSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(source='id', read_only=True)
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
            return obj.buyer_profile.first().preferred_locations
        except:
            return ""

    def get_budget_range(self, obj):
        try:
            return obj.buyer_profile.first().budget_range
        except:
            return ""
