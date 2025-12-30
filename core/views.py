from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.core.serializers.json import DjangoJSONEncoder
from core.mixins import BuyerRequiredMixin, SellerRequiredMixin, RealtorRequiredMixin, PartnerRequiredMixin, AdminRequiredMixin
from api.v1.serializer import SellerProfileSerializer

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

class BuyerPropertySearchView(BuyerRequiredMixin, TemplateView):
    template_name = "buyer-property-search.html"

class PublicPropertySearchView(TemplateView):
    template_name = "public-property-search.html"

class PropertyDetailView(TemplateView):
    template_name = "property-detail.html"

class BuyerFavoritesView(BuyerRequiredMixin, TemplateView):
    template_name = "buyer-favorites.html"

class BuyerSettingsView(BuyerRequiredMixin, TemplateView):
    template_name = "buyer-settings.html"

class SellerDashboardView(SellerRequiredMixin, TemplateView):
    template_name = "seller-dashboard.html"
    extra_context = {'active_page': 'dashboard'}

class SellerPropertyView(SellerRequiredMixin, TemplateView):
    template_name = "seller-property.html"
    extra_context = {'active_page': 'properties'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'seller_profile'):
            context['seller_profile'] = self.request.user.seller_profile
            
            try:
                serializer = SellerProfileSerializer(self.request.user.seller_profile)
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
