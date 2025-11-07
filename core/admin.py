from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BaseUserDetails, Address

# Register your models here.

@admin.register(BaseUserDetails)
class BaseUserDetailsAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_verified')
    list_filter = ('role', 'is_active', 'is_verified', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'is_verified', 'is_updated')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'country', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'country', 'state')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'city', 'address')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
