from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.core.serializers.json import DjangoJSONEncoder
from core.models import User
from core.mixins import RoleRequiredMixin, BuyerRequiredMixin, SellerRequiredMixin, RealtorRequiredMixin, PartnerRequiredMixin, AdminRequiredMixin
from api.v1.serializer import SellerProfileSerializer
from api.models import PropertyView, SellerProfile
from django.utils import timezone

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class IndexView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

class LoginView(TemplateView):
    template_name = "login.html"

class SignupView(TemplateView):
    template_name = "signup.html"

class BuyerDashboardView(BuyerRequiredMixin, TemplateView):
    template_name = "buyer-dashboard.html"

class BuyerPropertySearchView(RoleRequiredMixin, TemplateView):
    allowed_roles = [User.UserRole.BUYER, User.UserRole.REALTOR]
    template_name = "buyer-property-search.html"

class PublicPropertySearchView(TemplateView):
    template_name = "public-property-search.html"

class PropertyDetailView(TemplateView):
    template_name = "property-detail.html"

    def get(self, request, *args, **kwargs):
        property_id = request.GET.get('id')
        if property_id:
            try:
                seller_profile = SellerProfile.objects.get(pk=property_id)
                ip_address = get_client_ip(request)
                
                # Record unique view
                PropertyView.objects.get_or_create(
                    seller_profile=seller_profile,
                    ip_address=ip_address
                )
            except Exception as e:
                pass 
                
        return super().get(request, *args, **kwargs)

class BuyerFavoritesView(BuyerRequiredMixin, TemplateView):
    template_name = "buyer-favorites.html"

class BuyerSettingsView(BuyerRequiredMixin, TemplateView):
    template_name = "buyer-settings.html"

class SellerDashboardView(SellerRequiredMixin, TemplateView):
    template_name = "seller-dashboard.html"
    extra_context = {'active_page': 'dashboard'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'seller_profile'):
            profile = self.request.user.seller_profile
            
            # Total Views
            context['total_views'] = profile.views.count() if hasattr(profile, 'views') else 0
            
            # Avg Days on Market
            if profile.has_active_listing:
                days = (timezone.now() - profile.created_at).days
                context['avg_days_on_market'] = max(0, days)
            else:
                context['avg_days_on_market'] = 0
                
        return context

class SellerPropertyView(SellerRequiredMixin, TemplateView):
    template_name = "seller-property.html"
    extra_context = {'active_page': 'properties'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'seller_profile'):
            profile = self.request.user.seller_profile
            context['seller_profile'] = profile
            context['total_views'] = profile.views.count() if hasattr(profile, 'views') else 0
            
            try:
                serializer = SellerProfileSerializer(profile)
                context['seller_profile_json'] = json.dumps(serializer.data, cls=DjangoJSONEncoder)
            except Exception as e:
                print(f"Error serializing seller profile: {e}")
                context['seller_profile_json'] = "{}"
            
        return context

class SellerSettingsView(SellerRequiredMixin, TemplateView):
    template_name = "seller-settings.html"
    extra_context = {'active_page': 'settings'}

class RealtorDashboardView(RealtorRequiredMixin, TemplateView):
    template_name = "realtor-dashboard.html"
    extra_context = {'active_page': 'dashboard'}

class RealtorSettingsView(RealtorRequiredMixin, TemplateView):
    template_name = "realtor-settings.html"
    extra_context = {'active_page': 'settings'}

class RealtorClientsView(RealtorRequiredMixin, TemplateView):
    template_name = "realtor-clients.html"
    extra_context = {'active_page': 'clients'}

class PartnerDashboardView(PartnerRequiredMixin, TemplateView):
    template_name = "partner-dashboard.html"
    extra_context = {'active_page': 'dashboard'}

class PartnerSettingsView(PartnerRequiredMixin, TemplateView):
    template_name = "partner-settings.html"
    extra_context = {'active_page': 'settings'}

class PartnersView(TemplateView):
    template_name = "partners.html"

class TermsOfServiceView(TemplateView):
    template_name = "terms-of-service.html"

class PrivacyPolicyView(TemplateView):
    template_name = "privacy-policy.html"

class CustomAdminPricingView(AdminRequiredMixin, TemplateView):
    template_name = "custom_admin_pricing.html"

class BuyerAddRealtorView(BuyerRequiredMixin, TemplateView):
    template_name = "buyer-add-realtor.html"
    extra_context = {'active_page': 'add_realtor'}

class RealtorRequestsView(RealtorRequiredMixin, TemplateView):
    template_name = "realtor-requests.html"
    extra_context = {'active_page': 'requests'}
