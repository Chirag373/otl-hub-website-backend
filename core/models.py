from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role(models.TextChoices):
        ADMIN = "ADMIN", "admin"
        BUYER = "BUYER", "buyer"
        SELLER = "SELLER", "seller"
        REALTOR = "REALTOR", "realtor"
        PARTNER = "PARTNER", "partner"

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class BaseUserDetails(AbstractUser, BaseModel):
    role = models.CharField(max_length=255, choices=Role.choices, default=Role.BUYER)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_updated = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

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

class MembershipStatus(BaseModel):
    user = models.ForeignKey(BaseUserDetails, on_delete=models.CASCADE)
    partner_since = models.DateField(null=True, blank=True)
    partner_until = models.DateField(null=True, blank=True)
    fee_paid = models.BooleanField(default=False)
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"
    
    class Meta:
        verbose_name = "Membership Status"
        verbose_name_plural = "Membership Statuses"
        ordering = ["-created_at"]



    



        

