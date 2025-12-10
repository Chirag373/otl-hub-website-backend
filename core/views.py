from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

class LoginView(TemplateView):
    template_name = "login.html"

class SignupView(TemplateView):
    template_name = "signup.html"

class BuyerDashboardView(TemplateView):
    template_name = "buyer-dashboard.html"

class SellerDashboardView(TemplateView):
    template_name = "seller-dashboard.html"

class RealtorDashboardView(TemplateView):
    template_name = "realtor-dashboard.html"

class PartnerDashboardView(TemplateView):
    template_name = "partner-dashboard.html"

class PartnersView(TemplateView):
    template_name = "partners.html"
