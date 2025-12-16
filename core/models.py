from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Extended User model with role-based authentication"""

    class UserRole(models.TextChoices):
        BUYER = "BUYER", _("Buyer")
        REALTOR = "REALTOR", _("Realtor")
        SELLER = "SELLER", _("Seller")
        PARTNER = "PARTNER", _("Partner")

    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        help_text=_("User role in the platform"),
    )
    phone_number = models.CharField(max_length=20, help_text=_("Contact phone number"))

    # Common fields
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # OTP Verification
    otp = models.CharField(max_length=8, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email", "role"]),
        ]

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


class Subscription(models.Model):
    """Track subscription payments and details"""

    class SubscriptionType(models.TextChoices):
        BUYER_BASIC = "BUYER_BASIC", _("Buyer Basic Plan")
        BUYER_PRO = "BUYER_PRO", _("Buyer Pro Plan")
        REALTOR_PROFESSIONAL = "REALTOR_PROFESSIONAL", _("Realtor Professional")
        SELLER_LISTING = "SELLER_LISTING", _("Seller Property Listing")
        PARTNER_BUSINESS = "PARTNER_BUSINESS", _("Partner Business Subscription")

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        COMPLETED = "COMPLETED", _("Completed")
        FAILED = "FAILED", _("Failed")
        REFUNDED = "REFUNDED", _("Refunded")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    subscription_type = models.CharField(
        max_length=50, choices=SubscriptionType.choices
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    setup_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    transaction_id = models.CharField(
        max_length=255, blank=True, help_text=_("Payment gateway transaction ID")
    )

    # Subscription period
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subscriptions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "subscription_type"]),
            models.Index(fields=["payment_status"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.get_subscription_type_display()}"


class PendingSignup(models.Model):
    """Temporary storage for signup data before OTP verification"""
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=8)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    signup_data = models.JSONField()

    class Meta:
        db_table = "pending_signups"
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"Pending: {self.email}"
