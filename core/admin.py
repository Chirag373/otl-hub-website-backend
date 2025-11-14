from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Subscription


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model"""

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "date_joined",
    )
    list_filter = ("role", "is_active", "is_staff", "date_joined")
    search_fields = ("email", "username", "first_name", "last_name", "phone_number")
    ordering = ("-created_at",)

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Additional Info",
            {"fields": ("role", "phone_number", "created_at", "updated_at")},
        ),
    )
    readonly_fields = ("created_at", "updated_at", "date_joined")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin interface for Subscription model"""

    list_display = (
        "user",
        "subscription_type",
        "amount",
        "payment_status",
        "start_date",
        "end_date",
        "created_at",
    )
    list_filter = ("subscription_type", "payment_status", "created_at")
    search_fields = ("user__email", "transaction_id")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"

    fieldsets = (
        ("User Information", {"fields": ("user",)}),
        (
            "Subscription Details",
            {
                "fields": (
                    "subscription_type",
                    "amount",
                    "setup_fee",
                    "start_date",
                    "end_date",
                )
            },
        ),
        ("Payment Information", {"fields": ("payment_status", "transaction_id")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
