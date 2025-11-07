from django.db import models

from core.models import BaseModel, BaseUserDetails, BudgetRange
# Create your models here.
class BuyerProfile(BaseModel):
    user = models.ForeignKey(BaseUserDetails, on_delete=models.CASCADE, related_name='buyer_profile')
    budget_range = models.CharField(max_length=50, choices=BudgetRange.choices, null=True, blank=True)
    preferred_locations = models.TextField(null=True, blank=True, help_text="Comma-separated list of preferred locations")
    property_type = models.CharField(max_length=500, null=True, blank=True, help_text="Comma-separated list of property types (HOUSE, CONDO, TOWNHOUSE, APARTMENT, LAND, COMMERCIAL)") 

    def __str__(self):
        return f"Buyer Profile - {self.user.get_full_name()}"
    
    class Meta:
        verbose_name = "Buyer Profile"
        verbose_name_plural = "Buyer Profiles"
        ordering = ["-created_at"]

class SellerProfile(BaseModel):
    user = models.ForeignKey(BaseUserDetails, on_delete=models.CASCADE, related_name='seller_profile')
    property_type = models.CharField(max_length=500, null=True, blank=True, help_text="Comma-separated list of property types (HOUSE, CONDO, TOWNHOUSE, APARTMENT, LAND, COMMERCIAL)")
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    seller_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Seller Profile - {self.user.get_full_name()}"

    class Meta:
        verbose_name = "Seller Profile"
        verbose_name_plural = "Seller Profiles"
        ordering = ["-created_at"]

class RealtorProfile(BaseModel):
    user = models.OneToOneField(BaseUserDetails, on_delete=models.CASCADE, related_name='realtor_profile')
    license_number = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    professional_summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Realtor Profile - {self.user.get_full_name()}"
    
    class Meta:
        verbose_name = "Realtor Profile"
        verbose_name_plural = "Realtor Profiles"
        ordering = ["-created_at"]

class PartnerProfile(BaseModel):
    user = models.OneToOneField(BaseUserDetails, on_delete=models.CASCADE, related_name='partner_profile')
    company_name = models.CharField(max_length=255, null=True, blank=True)
    service_areas = models.TextField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    business_license_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Partner Profile - {self.company_name or self.user.get_full_name()}"

    class Meta:
        verbose_name = "Partner Profile"
        verbose_name_plural = "Partner Profiles"
        ordering = ["-created_at"]


