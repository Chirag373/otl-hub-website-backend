from django.contrib import admin
from .models import BuyerProfile, RealtorProfile, SellerProfile, PartnerProfile


@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    """Admin interface for BuyerProfile model"""

    list_display = (
        "user",
        "preferred_location",
        "budget_range",

        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "preferred_location",
    )
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("User Information", {"fields": ("user",)}),
        ("Preferences", {"fields": ("preferred_location", "budget_range")}),

        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(RealtorProfile)
class RealtorProfileAdmin(admin.ModelAdmin):
    """Admin interface for RealtorProfile model"""

    list_display = (
        "user",
        "license_number",
        "company_brokerage",
        "years_of_experience",

        "created_at",
    )
    list_filter = ("years_of_experience", "created_at")
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "license_number",
        "company_brokerage",
    )
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("User Information", {"fields": ("user",)}),
        (
            "Professional Details",
            {"fields": ("license_number", "company_brokerage", "years_of_experience")},
        ),

        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    """Admin interface for SellerProfile model"""

    list_display = (
        "user",
        "property_type",
        "property_location",
        "estimated_value",
        "has_active_listing",
        "created_at",
    )
    list_filter = ("property_type", "has_active_listing", "created_at")
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "property_location",
    )
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("User Information", {"fields": ("user",)}),
        (
            "Property Details",
            {"fields": ("property_type", "property_location", "estimated_value")},
        ),
        ("Listing Status", {"fields": ("has_active_listing", "listing_created_at")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):
    """Admin interface for PartnerProfile model"""

    list_display = (
        "user",
        "company_name",
        "partnership_type",

        "created_at",
    )
    list_filter = ("partnership_type", "created_at")
    search_fields = ("user__email", "company_name", "service_areas")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("User Information", {"fields": ("user",)}),
        (
            "Business Details",
            {"fields": ("company_name", "partnership_type", "service_areas")},
        ),

        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
