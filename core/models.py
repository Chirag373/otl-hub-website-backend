import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Role(models.TextChoices):
        ADMIN = "ADMIN", "admin"
        BUYER = "BUYER", "buyer"
        SELLER = "SELLER", "seller"
        REALTOR = "REALTOR", "realtor"
        PARTNER = "PARTNER", "partner"

class BudgetRange(models.TextChoices):
        RANGE_0_200K = "0-200000", "$0 - $200,000"
        RANGE_200K_400K = "200000-400000", "$200,000 - $400,000"
        RANGE_400K_600K = "400000-600000", "$400,000 - $600,000"
        RANGE_600K_800K = "600000-800000", "$600,000 - $800,000"
        RANGE_800K_1M = "800000-1000000", "$800,000 - $1,000,000"
        RANGE_1M_PLUS = "1000000+", "$1,000,000+"



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class BaseUserDetails(AbstractUser, BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=255, choices=Role.choices, default=Role.BUYER)
    location = models.CharField(max_length=255, null=True, blank=True)
    is_updated = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

class Address(BaseModel):
    user = models.ForeignKey(BaseUserDetails, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.country}, {self.postal_code}"
    
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        ordering = ["-created_at"]
