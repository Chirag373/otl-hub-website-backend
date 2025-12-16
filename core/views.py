from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

class LoginView(TemplateView):
    template_name = "login.html"

class SignupView(TemplateView):
    template_name = "signup.html"

from django.contrib.auth.mixins import LoginRequiredMixin

class BuyerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "buyer-dashboard.html"

class BuyerPropertySearchView(LoginRequiredMixin, TemplateView):
    template_name = "buyer-property-search.html"

class BuyerFavoritesView(LoginRequiredMixin, TemplateView):
    template_name = "buyer-favorites.html"

class BuyerSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "buyer-settings.html"

class SellerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "seller-dashboard.html"
    extra_context = {'active_page': 'dashboard'}

class SellerSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "seller-settings.html"
    extra_context = {'active_page': 'settings'}

class RealtorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "realtor-dashboard.html"
    extra_context = {'active_page': 'dashboard'}

class RealtorSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "realtor-settings.html"
    extra_context = {'active_page': 'settings'}

class PartnerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "partner-dashboard.html"
    extra_context = {'active_page': 'dashboard'}

class PartnerSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "partner-settings.html"
    extra_context = {'active_page': 'settings'}

class PartnersView(TemplateView):
    template_name = "partners.html"

class TermsOfServiceView(TemplateView):
    template_name = "terms-of-service.html"

class PrivacyPolicyView(TemplateView):
    template_name = "privacy-policy.html"
