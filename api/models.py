from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class BuyerProfile(models.Model):
    class BudgetRange(models.TextChoices):
        RANGE_0_200K = "0-200000", "$0 - $200,000"
        RANGE_200K_400K = "200000-400000", "$200,000 - $400,000"
        RANGE_400K_600K = "400000-600000", "$400,000 - $600,000"
        RANGE_600K_800K = "600000-800000", "$600,000 - $800,000"
        RANGE_800K_1M = "800000-1000000", "$800,000 - $1,000,000"
        RANGE_1M_PLUS = "1000000+", "$1,000,000+"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buyer_profile")
    preferred_location = models.CharField(max_length=255, blank=True, help_text="City, State for property search")
    budget_range = models.CharField(max_length=100, blank=True, choices=BudgetRange.choices)
    
    # Subscription/Membership fields
    is_membership_active = models.BooleanField(default=False)
    membership_end_date = models.DateTimeField(null=True, blank=True)
    
    access_pass_expiry = models.DateTimeField(null=True, blank=True, help_text='Expiration date of the current Access Pass')
    access_pass_extensions_used = models.IntegerField(default=0, help_text='Number of extensions used (max 2)')
    
    assigned_agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_buyers")
    favorites = models.ManyToManyField("SellerProfile", blank=True, related_name="favorited_by")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "buyer_profiles"
        
    def __str__(self):
        return f"{self.user.email} - Buyer"


class SellerProfile(models.Model):
    class PropertyType(models.TextChoices):
        SINGLE_FAMILY = "SINGLE_FAMILY", "Single Family"
        CONDO = "CONDO", "Condo"
        TOWNHOME = "TOWNHOME", "Townhome"
        APARTMENT_UNIT = "APARTMENT_UNIT", "Apartment Unit"
        
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seller_profile")
    
    # Address
    address_number = models.CharField(max_length=50, blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    county = models.CharField(max_length=100, blank=True)
    
    property_type = models.CharField(max_length=50, blank=True, choices=PropertyType.choices)
    property_description = models.TextField(blank=True)
    
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    
    # Extended
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    sqft = models.IntegerField(default=0)
    garage_spaces = models.IntegerField(default=0)
    property_features = models.JSONField(default=dict, blank=True)
    
    has_active_listing = models.BooleanField(default=False)
    leaseback_required = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "seller_profiles"

    def __str__(self):
        return f"{self.user.email} - Seller"


class RealtorProfile(models.Model):
    class ExperienceLevel(models.TextChoices):
        ENTRY = "ENTRY", "0-2 years"
        INTERMEDIATE = "INTERMEDIATE", "3-5 years"
        EXPERIENCED = "EXPERIENCED", "6-10 years"
        EXPERT = "EXPERT", "10+ years"
        
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="realtor_profile")
    license_number = models.CharField(max_length=100, unique=True, help_text="Real estate license number")
    company_brokerage = models.CharField(max_length=255, help_text="Company or brokerage name")
    years_of_experience = models.CharField(max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.ENTRY)
    
    description = models.TextField(blank=True)
    
    is_active_subscription = models.BooleanField(default=False)
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "realtor_profiles"

    def __str__(self):
        return f"{self.user.email} - Realtor"


class PartnerProfile(models.Model):
    class PartnershipType(models.TextChoices):
        REAL_ESTATE_AGENT = "REAL_ESTATE_AGENT", "Real Estate Agency"
        MORTGAGE = "MORTGAGE", "Mortgage Lender"
        HOME_INSPECTION = "HOME_INSPECTION", "Home Inspector"
        CONTRACTOR = "CONTRACTOR", "Contractor"
        MOVING_COMPANY = "MOVING_COMPANY", "Moving Company"
        PROPERTY_APPRAISER = "PROPERTY_APPRAISER", "Property Appraiser"
        OTHER = "OTHER", "Other"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="partner_profile")
    company_name = models.CharField(max_length=255, help_text="Business or company name")
    partnership_type = models.CharField(max_length=50, choices=PartnershipType.choices)
    service_areas = models.TextField(help_text="Cities or regions served")
    
    website_url = models.URLField(blank=True)
    business_license_number = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "partner_profiles"

    def __str__(self):
        return f"{self.user.email} - Partner"

class PropertyImage(models.Model):
    seller_profile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'property_images'


class AccessPassType(models.Model):
    name = models.CharField(max_length=50) # e.g. "Basic", "Pro"
    slug = models.SlugField(unique=True) # e.g. "basic", "pro"
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    days_duration = models.IntegerField(default=30)
    
    # Extension logic
    extension_days = models.IntegerField(default=15, help_text="Number of days given per extension")
    extension_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_extensions = models.IntegerField(default=2)
    
    # Unlocks
    properties_limit = models.IntegerField(default=10, help_text="Number of properties this pass unlocks")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "access_pass_types"

    def __str__(self):
        return f"{self.name} Access Pass"


class PricingPlan(models.Model):
    PLAN_TYPES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('realtor', 'Realtor'),
        ('partner', 'Partner'),
    )

    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, unique=True)
    
    # Generic fees (used by multiple roles)
    setup_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    access_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Specific to Seller
    listing_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Specific to Buyer
    buyer_upfront_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="For Buyer Membership (upfront)")
    buyer_monthly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="For Buyer Membership (monthly)")
    
    # New: Configurable trial/min months
    buyer_min_months = models.IntegerField(default=3, help_text="Minimum months for initial subscription")
    
    # buyer_access_pass_price is likely obsolete if we use AccessPassType, 
    # but keeping it for backward compat or as a default if no types found
    buyer_access_pass_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Legacy: Basic Access Pass Price")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pricing_plans"

    def __str__(self):
        return f"{self.get_plan_type_display()} Pricing"


class PropertyView(models.Model):
    seller_profile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "property_views"
        unique_together = ('seller_profile', 'ip_address')
        indexes = [
            models.Index(fields=["seller_profile", "ip_address"]),
        ]
