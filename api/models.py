from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from core.models import User


class BuyerProfile(models.Model):
    """Profile specific to Buyer users"""

    class BudgetRange(models.TextChoices):
        BUDGET_RANGE_STEP_1 = '0-200000', '$0 - $200,000'
        BUDGET_RANGE_STEP_2 = '200000-400000', '$200,000 - $400,000'
        BUDGET_RANGE_STEP_3 = '400000-600000', '$400,000 - $600,000'
        BUDGET_RANGE_STEP_4 = '600000-800000', '$600,000 - $800,000'
        BUDGET_RANGE_STEP_5 = '800000-1000000', '$800,000 - $1,000,000'
        BUDGET_RANGE_STEP_6 = '1000000+', '$1,000,000+'
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='buyer_profile',
        limit_choices_to={'role': User.UserRole.BUYER}
    )
    preferred_location = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("City, State for property search")
    )
    budget_range = models.CharField(
        max_length=100,
        blank=True,
        choices=BudgetRange.choices,
        help_text=_("Budget range for property purchase")
    )

    # Assigned realtor/agent
    assigned_agent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_buyers',
        limit_choices_to={'role': User.UserRole.REALTOR},
        help_text=_("Assigned realtor/agent for this buyer")
    )

    # Subscription details
    subscription_plan = models.CharField(
        max_length=50,
        choices=[
            ('BASIC', 'Basic Plan'),
            ('PRO', 'Pro Plan'),
        ],
        default='BASIC'
    )
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'buyer_profiles'
    
    def __str__(self):
        return f"Buyer Profile: {self.user.email}"


class RealtorProfile(models.Model):
    """Profile specific to Realtor users"""
    
    class ExperienceLevel(models.TextChoices):
        ENTRY = 'ENTRY', _('0-2 years')
        INTERMEDIATE = 'INTERMEDIATE', _('3-5 years')
        EXPERIENCED = 'EXPERIENCED', _('6-10 years')
        EXPERT = 'EXPERT', _('10+ years')
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='realtor_profile',
        limit_choices_to={'role': User.UserRole.REALTOR}
    )
    license_number = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Real estate license number")
    )
    company_brokerage = models.CharField(
        max_length=255,
        help_text=_("Company or brokerage name")
    )
    years_of_experience = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.ENTRY
    )
    
    # Subscription details
    subscription_active = models.BooleanField(default=False)
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'realtor_profiles'
        indexes = [
            models.Index(fields=['license_number']),
        ]
    
    def __str__(self):
        return f"Realtor Profile: {self.user.email}"


class SellerProfile(models.Model):
    """Profile specific to Seller users"""
    
    class PropertyType(models.TextChoices):
        RESIDENTIAL = 'RESIDENTIAL', _('Residential')
        COMMERCIAL = 'COMMERCIAL', _('Commercial')
        LAND = 'LAND', _('Land')
        MULTI_FAMILY = 'MULTI_FAMILY', _('Multi-Family')
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='seller_profile',
        limit_choices_to={'role': User.UserRole.SELLER}
    )
    property_type = models.CharField(
        max_length=50,
        choices=PropertyType.choices,
        blank=True
    )
    estimated_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    property_location = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("City, State where property is located")
    )
    
    # Listing status
    has_active_listing = models.BooleanField(default=False)
    listing_created_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'seller_profiles'
    
    def __str__(self):
        return f"Seller Profile: {self.user.email}"


class PartnerProfile(models.Model):
    """Profile specific to Partner users (business partners/service providers)"""
    
    class PartnershipType(models.TextChoices):
        REAL_ESTATE_AGENT = 'REAL_ESTATE_AGENT', _('Real Estate Agent')
        MORTGAGE = 'MORTGAGE', _('Mortgage Lender')
        HOME_INSPECTION = 'HOME_INSPECTION', _('Home Inspection')
        PROPERTY_APPRAISER = 'PROPERTY_APPRAISER', _('Property Appraiser')
        CONTRACTOR = 'CONTRACTOR', _('Contractor')
        MOVING_COMPANY = 'MOVING_COMPANY', _('Moving Company')
        OTHER = 'OTHER', _('Other Services')
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='partner_profile',
        limit_choices_to={'role': User.UserRole.PARTNER}
    )
    company_name = models.CharField(
        max_length=255,
        help_text=_("Business or company name")
    )
    partnership_type = models.CharField(
        max_length=50,
        choices=PartnershipType.choices
    )
    service_areas = models.TextField(
        help_text=_("Cities or regions served (comma-separated)")
    )
    website_url = models.URLField(
        max_length=255,
        blank=True,
        help_text=_("Website URL")
    )
    business_license_number = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Business license number"),
        default=""
    )
    
    # Subscription details
    subscription_active = models.BooleanField(default=False)
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'partner_profiles'
        indexes = [
            models.Index(fields=['partnership_type']),
        ]
    
    def __str__(self):
        return f"Partner Profile: {self.company_name}"
