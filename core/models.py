from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Extended User model with role-based authentication"""
    username = None

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

    # Stripe
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email", "role"]),
        ]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


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
