from rest_framework import serializers
from django.db import transaction
from core.models import User, PendingSignup
from api.models import BuyerProfile, RealtorProfile, SellerProfile, PartnerProfile, PropertyImage
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from api.models import RealtorProfile

from django.utils import timezone
from datetime import timedelta
import secrets
import json


class UserResponseSerializer(serializers.ModelSerializer):
    """
    Standard serializer for returning user data in API responses
    """
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone_number", "role"]


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=8)  # Changed to 8 to match generation

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')

        # 1. Check if pending signup exists
        try:
            pending_signup = PendingSignup.objects.get(email=email)
        except PendingSignup.DoesNotExist:
            # Check if User exists and is active (already verified)
            if User.objects.filter(email=email, is_active=True).exists():
                 raise serializers.ValidationError({"message": "Account is already verified."})
            raise serializers.ValidationError({"email": "No pending verification found for this email."})

        # 2. Check if OTP is expired
        if pending_signup.otp_created_at and (timezone.now() > pending_signup.otp_created_at + timedelta(minutes=10)):
            raise serializers.ValidationError({"otp": "OTP has expired. Please signup again."})

        # 3. Verify OTP (Safe Comparison)
        if not secrets.compare_digest(str(pending_signup.otp), str(otp)):
            raise serializers.ValidationError({"otp": "Invalid OTP."})

        # Attach the pending signup object to the validated data for the View to use
        attrs['pending_signup'] = pending_signup
        return attrs


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup
    """

    password = serializers.CharField(write_only=True, min_length=8, validators=[validate_password])
    role = serializers.ChoiceField(choices=User.UserRole.choices)
    license_number = serializers.CharField(required=False, allow_blank=True)
    company_brokerage = serializers.CharField(required=False, allow_blank=True)
    preferred_location = serializers.CharField(required=False, allow_blank=True)
    property_type = serializers.ChoiceField(
        choices=SellerProfile.PropertyType.choices, required=False, allow_blank=True
    )
    budget_range = serializers.ChoiceField(
        choices=BuyerProfile.BudgetRange.choices, required=False, allow_blank=True
    )
    years_of_experience = serializers.ChoiceField(
        choices=RealtorProfile.ExperienceLevel.choices, required=False
    )
    estimated_value = serializers.DecimalField(
        max_digits=15, decimal_places=2, required=False
    )
    property_location = serializers.CharField(required=False, allow_blank=True)
    company_name = serializers.CharField(required=False, allow_blank=True)
    partnership_type = serializers.ChoiceField(
        choices=PartnerProfile.PartnershipType.choices, required=False
    )
    service_areas = serializers.CharField(required=False, allow_blank=True)
    website_url = serializers.URLField(required=False, allow_blank=True)
    business_license_number = serializers.CharField(required=False, allow_blank=True)
    selected_plan = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "license_number",
            "company_brokerage",
            "preferred_location",
            "property_type",
            "budget_range",
            "years_of_experience",
            "estimated_value",
            "property_location",
            "company_name",
            "partnership_type",
            "service_areas",
            "website_url",
            "business_license_number",
            "selected_plan",
        ]

    def validate(self, data):
        role = data.get("role")

        if role == User.UserRole.BUYER:
            if not data.get("preferred_location"):
                raise serializers.ValidationError(
                    {"preferred_location": "Preferred location required for buyers."}
                )
            if not data.get("budget_range"):
                raise serializers.ValidationError(
                    {"budget_range": "Budget range required for buyers."}
                )

        elif role == User.UserRole.REALTOR:
            if not data.get("license_number"):
                raise serializers.ValidationError(
                    {"license_number": "License number required for realtors."}
                )
            if not data.get("company_brokerage"):
                raise serializers.ValidationError(
                    {"company_brokerage": "Company brokerage required for realtors."}
                )
            if data.get("years_of_experience") is None:
                raise serializers.ValidationError(
                    {
                        "years_of_experience": "Years of experience required for realtors."
                    }
                )

        elif role == User.UserRole.SELLER:
            if not data.get("property_type"):
                raise serializers.ValidationError(
                    {"property_type": "Property type required for sellers."}
                )
            if data.get("estimated_value") is None:
                raise serializers.ValidationError(
                    {"estimated_value": "Estimated value required for sellers."}
                )
            if not data.get("property_location"):
                raise serializers.ValidationError(
                    {"property_location": "Property location required for sellers."}
                )

        elif role == User.UserRole.PARTNER:
            if not data.get("company_name"):
                raise serializers.ValidationError(
                    {"company_name": "Company name required for partners."}
                )
            if not data.get("partnership_type"):
                raise serializers.ValidationError(
                    {"partnership_type": "Partnership type required for partners."}
                )
            if not data.get("service_areas"):
                raise serializers.ValidationError(
                    {"service_areas": "Service areas required for partners."}
                )
            if not data.get("website_url"):
                raise serializers.ValidationError(
                    {"website_url": "Website URL required for partners."}
                )
            if not data.get("business_license_number"):
                raise serializers.ValidationError(
                    {
                        "business_license_number": "Business license number required for partners."
                    }
                )

        return data

    @transaction.atomic
    def create(self, validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop("password")

        # Pop all role-specific fields
        license_number = validated_data.pop("license_number", None)
        company_brokerage = validated_data.pop("company_brokerage", None)
        preferred_location = validated_data.pop("preferred_location", None)
        property_type = validated_data.pop("property_type", None)
        budget_range = validated_data.pop("budget_range", None)
        years_of_experience = validated_data.pop("years_of_experience", None)
        estimated_value = validated_data.pop("estimated_value", None)
        property_location = validated_data.pop("property_location", None)
        company_name = validated_data.pop("company_name", None)
        partnership_type = validated_data.pop("partnership_type", None)
        service_areas = validated_data.pop("service_areas", None)
        website_url = validated_data.pop("website_url", None)
        business_license_number = validated_data.pop("business_license_number", None)
        selected_plan = validated_data.pop("selected_plan", None)

        # Create user using the manager's create_user method which handles hashing
        # and email normalization
        email = validated_data.pop("email")
        
        # Ensure we pass the required fields
        user = User.objects.create_user(
            email=email,
            password=password,
            role=role,
            is_active=False,  # Set inactive until OTP verification
            **validated_data,
        )

        # Create profiles (validation ensures these values exist)
        if role == User.UserRole.BUYER:
            BuyerProfile.objects.create(
                user=user,
                preferred_location=preferred_location,
                budget_range=budget_range,
            )
        elif role == User.UserRole.REALTOR:
            RealtorProfile.objects.create(
                user=user,
                license_number=license_number,
                company_brokerage=company_brokerage,
                years_of_experience=years_of_experience,

            )
        elif role == User.UserRole.SELLER:
            city = ""
            state = ""
            if property_location:
                parts = property_location.split(',')
                if len(parts) >= 1:
                    city = parts[0].strip()
                if len(parts) >= 2:
                    state = parts[1].strip()
            
            SellerProfile.objects.create(
                user=user,
                property_type=property_type,
                estimated_value=estimated_value,
                city=city,
                state=state,
            )
        elif role == User.UserRole.PARTNER:
            PartnerProfile.objects.create(
                user=user,
                company_name=company_name,
                partnership_type=partnership_type,
                service_areas=service_areas,
                website_url=website_url,
                business_license_number=business_license_number,
            )

        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                _("Both email and password are required.")
            )

        # authenticate() uses AUTHENTICATION_BACKENDS; works because USERNAME_FIELD = 'email'
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(_("Invalid email or password."))

        if not user.is_active:
            raise serializers.ValidationError(_("User account is disabled."))

        attrs["user"] = user
        return attrs


class AgentSerializer(serializers.ModelSerializer):
    """Serializer for assigned realtor/agent information"""

    name = serializers.SerializerMethodField()
    phone = serializers.CharField(source="user.phone_number", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    brokerage_company = serializers.CharField(
        source="company_brokerage", read_only=True
    )

    class Meta:
        model = RealtorProfile
        fields = ["name", "phone", "email", "brokerage_company"]

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"





class BuyerProfileSerializer(serializers.ModelSerializer):
    """Serializer for Buyer Profile data"""

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number")
    role = serializers.CharField(source="user.role", read_only=True)
    member_since = serializers.DateTimeField(
        source="user.date_joined", read_only=True, format="%B %Y"
    )
    location = serializers.CharField(
        source="preferred_location", required=False, allow_blank=True
    )
    budget_range = serializers.SerializerMethodField()
    access_pass_expiry = serializers.DateTimeField(read_only=True)

    # Nested serializers for agent
    agent = serializers.SerializerMethodField()


    class Meta:
        model = BuyerProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "member_since",
            "location",
            "budget_range",
            "access_pass_expiry",
            "agent",

        ]

    def get_agent(self, obj):
        """Get assigned agent/realtor information"""
        # Assuming there's a relationship between BuyerProfile and RealtorProfile
        # You may need to adjust this based on your actual model relationships
        if hasattr(obj, "assigned_agent") and obj.assigned_agent:

            try:
                realtor = RealtorProfile.objects.get(user=obj.assigned_agent)
                return AgentSerializer(realtor).data
            except RealtorProfile.DoesNotExist:
                return None
        return None

    def get_budget_range(self, obj):
        """Get formatted budget range display"""
        if obj.budget_range:
            # Get the display value from the choices
            for choice_value, choice_display in BuyerProfile.BudgetRange.choices:
                if choice_value == obj.budget_range:
                    return choice_display
        return obj.budget_range  # Return raw value if no match found



    def update(self, instance, validated_data):
        # Handle nested user data
        user_data = validated_data.pop("user", {})
        user = instance.user

        # Update user fields
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.phone_number = user_data.get("phone_number", user.phone_number)
        user.save()

        # Update profile fields
        instance.preferred_location = validated_data.get(
            "preferred_location", instance.preferred_location
        )
        instance.budget_range = validated_data.get(
            "budget_range", instance.budget_range
        )
        instance.save()

        return instance


class RealtorProfileSerializer(serializers.ModelSerializer):
    """Serializer for Realtor Profile data"""

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number")
    role = serializers.CharField(source="user.role", read_only=True)
    member_since = serializers.DateTimeField(
        source="user.date_joined", read_only=True, format="%B %Y"
    )
    brokerage_company = serializers.CharField(
        source="company_brokerage", required=False, allow_blank=True
    )
    license_number = serializers.CharField(required=False, allow_blank=True)
    experience = serializers.SerializerMethodField()
    years_of_experience = serializers.ChoiceField(
        choices=RealtorProfile.ExperienceLevel.choices, required=False, write_only=True
    )
    description = serializers.CharField(required=False, allow_blank=True)

    # Nested serializer for agent


    class Meta:
        model = RealtorProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "member_since",
            "brokerage_company",
            "license_number",
            "experience",
            "years_of_experience",
            "description",

        ]

    def get_experience(self, obj):
        """Get formatted experience level display"""
        if obj.years_of_experience:
            for choice_value, choice_display in RealtorProfile.ExperienceLevel.choices:
                if choice_value == obj.years_of_experience:
                    return choice_display
        return obj.years_of_experience



    def update(self, instance, validated_data):
        print(f"DEBUG: validated_data keys: {validated_data.keys()}")
        user_data = validated_data.pop("user", {})
        user = instance.user

        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.phone_number = user_data.get("phone_number", user.phone_number)
        user.save()

        instance.company_brokerage = validated_data.get(
            "company_brokerage", instance.company_brokerage
        )
        instance.license_number = validated_data.get(
            "license_number", instance.license_number
        )
        instance.years_of_experience = validated_data.get(
            "years_of_experience", instance.years_of_experience
        )
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        return instance


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ["id", "image", "is_primary"]


class SellerProfileSerializer(serializers.ModelSerializer):
    """Serializer for Seller Profile data"""

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number")
    role = serializers.CharField(source="user.role", read_only=True)
    member_since = serializers.DateTimeField(
        source="user.date_joined", read_only=True, format="%B %Y"
    )

    # Address fields
    address_number = serializers.CharField(required=False, allow_blank=True)
    street_address = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    zip_code = serializers.CharField(required=False, allow_blank=True)
    county = serializers.CharField(required=False, allow_blank=True)

    # Property details
    property_type = serializers.SerializerMethodField()
    property_type_val = serializers.CharField(source='property_type', read_only=True)
    property_type_input = serializers.ChoiceField(
        choices=SellerProfile.PropertyType.choices, required=False, write_only=True, source='property_type'
    )
    property_description = serializers.CharField(required=False, allow_blank=True)
    estimated_value = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True
    )

    # Extended Property Details
    bedrooms = serializers.IntegerField(required=False)
    bathrooms = serializers.DecimalField(max_digits=4, decimal_places=1, required=False)
    sqft = serializers.IntegerField(required=False)
    garage_spaces = serializers.IntegerField(required=False)
    property_features = serializers.JSONField(required=False)
    
    images = PropertyImageSerializer(many=True, read_only=True)
    upload_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )


    
    leaseback_required = serializers.BooleanField(required=False)

    # Nested serializer for properties

    
    has_active_listing = serializers.BooleanField(required=False)

    class Meta:
        model = SellerProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "member_since",
            "address_number",
            "street_address",
            "city",
            "state",
            "zip_code",
            "county",
            "property_type",
            "property_type_val",
            "property_type_input",
            "property_description",
            "estimated_value",
            "bedrooms",
            "bathrooms",
            "sqft",
            "garage_spaces",
            "property_features",
            "property_features",
            "images",
            "upload_images",

            "leaseback_required",

            "has_active_listing",
        ]

    def get_property_type(self, obj):
        """Get formatted property type display"""
        if obj.property_type:
            for choice_value, choice_display in SellerProfile.PropertyType.choices:
                if choice_value == obj.property_type:
                    return choice_display
        return obj.property_type





    def update(self, instance, validated_data):
        print(f"DEBUG: validated_data keys: {validated_data.keys()}")
        user_data = validated_data.pop("user", {})
        user = instance.user

        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.phone_number = user_data.get("phone_number", user.phone_number)
        user.save()

        instance.address_number = validated_data.get(
            "address_number", instance.address_number
        )
        instance.street_address = validated_data.get(
            "street_address", instance.street_address
        )
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.zip_code = validated_data.get("zip_code", instance.zip_code)
        instance.county = validated_data.get("county", instance.county)
        
        # NOTE: because we use source='...', the key in validated_data is the model field name (e.g. 'property_type'), not '_input'
        instance.property_type = validated_data.get(
            "property_type", instance.property_type
        )
        instance.property_description = validated_data.get(
            "property_description", instance.property_description
        )
        instance.estimated_value = validated_data.get(
            "estimated_value", instance.estimated_value
        )
        
        # New fields
        instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
        instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
        instance.sqft = validated_data.get("sqft", instance.sqft)
        instance.garage_spaces = validated_data.get("garage_spaces", instance.garage_spaces)
        
        # Safe JSON handling for property_features
        property_features = validated_data.get("property_features", instance.property_features)
        if isinstance(property_features, str):
            try:
                property_features = json.loads(property_features)
            except json.JSONDecodeError:
                pass # Keep as string or handle error
        instance.property_features = property_features
        

        instance.leaseback_required = validated_data.get(
            "leaseback_required", instance.leaseback_required
        )
        
        if 'has_active_listing' in validated_data:
            instance.has_active_listing = validated_data.get('has_active_listing')
            
        instance.save()
        
        # Image Upload Handling
        upload_images = validated_data.pop('upload_images', None)
        if upload_images:
            # Check limit
            current_count = instance.images.count()
            if current_count + len(upload_images) > 6:
                raise serializers.ValidationError("Maximum 6 images allowed.")
                
            for image in upload_images:
                PropertyImage.objects.create(seller_profile=instance, image=image)

        return instance


class PropertySearchSerializer(serializers.ModelSerializer):
    """
    Serializer for publicly searching properties (SellerProfiles)
    """
    id = serializers.IntegerField(read_only=True) # Use profile ID for consistency with favorites lookup
    title = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    price = serializers.DecimalField(source='estimated_value', max_digits=12, decimal_places=2, read_only=True)
    image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    type = serializers.CharField(source='property_type', read_only=True)
    features = serializers.JSONField(source='property_features', read_only=True)
    dateAdded = serializers.DateTimeField(source='created_at', read_only=True)
    description = serializers.CharField(source='property_description', read_only=True)
    
    seller_info = serializers.SerializerMethodField()
    is_locked = serializers.SerializerMethodField()

    class Meta:
        model = SellerProfile
        fields = [
            'id', 'title', 'location', 'price', 
            'bedrooms', 'bathrooms', 'sqft', 
            'image', 'images', 'type', 'features', 'dateAdded', 'description',
            'leaseback_required', 'seller_info', 'is_locked'
        ]

    def get_is_locked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return True
        
        user = request.user
        
        # If user is the owner (Seller), they can see it
        if user == obj.user:
            return False

        # If user is a Buyer, check access pass
        if user.role == 'BUYER':
            try:
                # We access the profile. Since request.user is shared across the request,
                # this should be efficient enough (cached after first access)
                if hasattr(user, 'buyer_profile'):
                     profile = user.buyer_profile
                     if profile.access_pass_expiry and profile.access_pass_expiry > timezone.now():
                         return False
            except BuyerProfile.DoesNotExist:
                pass
        
        # For other roles (e.g. Realtor, Partner, Admin), maybe unlocked?
        # Assuming for now only Paid Buyers can see details.
        # If you want Admin to see, add: if user.is_staff: return False
        if user.is_staff:
            return False

        return True

    def get_title(self, obj):
        # If locked, hide specific address and city
        if self.get_is_locked(obj):
             return "Exclusive Listing"

        if obj.street_address:
            return obj.street_address
        return f"Property in {obj.city}" if obj.city else "Unlisted Address"

    def get_location(self, obj):
        # Hide location if locked
        if self.get_is_locked(obj):
            return "Location Protected"

        parts = [p for p in [obj.city, obj.state] if p]
        return ", ".join(parts) if parts else "Location N/A"

    def get_seller_info(self, obj):
        if self.get_is_locked(obj):
            return None
        
        u = obj.user
        return {
            "first_name": u.first_name,
            "last_name": u.last_name,
            "email": u.email,
            "phone": u.phone_number
        }

    def get_image(self, obj):
        # optimistically get primary image, or first available
        primary_img = obj.images.filter(is_primary=True).first()
        if not primary_img:
            primary_img = obj.images.first()
        
        if primary_img and primary_img.image:
            return primary_img.image.url
        return None # Frontend can show placeholder

    def get_images(self, obj):
        # Images might give away location? usually fine.
        return [img.image.url for img in obj.images.all() if img.image]




class PartnerProfileSerializer(serializers.ModelSerializer):
    """Serializer for Partner Profile data"""
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number")
    role = serializers.CharField(source="user.role", read_only=True)
    member_since = serializers.DateTimeField(
        source="user.date_joined", read_only=True, format="%B %Y"
    )
    
    partnership_type_display = serializers.CharField(source='get_partnership_type_display', read_only=True)

    # Nested serializer for partnership type


    class Meta:
        model = PartnerProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "member_since",
            "company_name",
            "partnership_type",
            "partnership_type_display",
            "service_areas",
            "website_url",
            "business_license_number",

        ]



    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user

        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.phone_number = user_data.get("phone_number", user.phone_number)
        user.save()

        instance.company_name = validated_data.get("company_name", instance.company_name)
        instance.partnership_type = validated_data.get(
            "partnership_type", instance.partnership_type
        )
        instance.service_areas = validated_data.get(
            "service_areas", instance.service_areas
        )
        instance.website_url = validated_data.get("website_url", instance.website_url)
        instance.business_license_number = validated_data.get(
            "business_license_number", instance.business_license_number
        )
        instance.save()

        return instance


from api.models import PricingPlan, AccessPassType
from rest_framework import serializers

class AccessPassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessPassType
        fields = '__all__'

class PricingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPlan
        fields = '__all__'

