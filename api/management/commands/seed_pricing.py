from django.core.management.base import BaseCommand
from api.models import PricingPlan
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds or updates pricing plans in the database'

    def handle(self, *args, **options):
        self.stdout.write("Seeding/Updating Pricing Plans...")

        # Buyer Plan
        buyer, _ = PricingPlan.objects.get_or_create(plan_type='buyer')
        buyer.buyer_monthly_price = Decimal('40.00')
        buyer.buyer_upfront_price = Decimal('120.00') # 3 months * $40
        buyer.buyer_min_months = 3
        buyer.buyer_access_pass_price = Decimal('650.00')
        buyer.save()
        self.stdout.write(f"Updated Buyer Plan: {buyer.buyer_upfront_price} upfront, {buyer.buyer_monthly_price}/mo")

        # Seller Plan
        seller, _ = PricingPlan.objects.get_or_create(plan_type='seller')
        seller.setup_fee = Decimal('99.00')
        seller.listing_fee = Decimal('199.00')
        seller.save()
        self.stdout.write(f"Updated Seller Plan: {seller.setup_fee} setup, {seller.listing_fee} listing")

        # Realtor Plan
        realtor, _ = PricingPlan.objects.get_or_create(plan_type='realtor')
        realtor.setup_fee = Decimal('99.00')
        realtor.access_fee = Decimal('99.00')
        realtor.monthly_fee = Decimal('49.00')
        realtor.save()
        self.stdout.write(f"Updated Realtor Plan: {realtor.setup_fee} setup, {realtor.access_fee} access, {realtor.monthly_fee}/mo")

        # Partner Plan
        partner, _ = PricingPlan.objects.get_or_create(plan_type='partner')
        partner.setup_fee = Decimal('199.00')
        partner.access_fee = Decimal('299.00')
        partner.monthly_fee = Decimal('99.00')
        partner.save()
        self.stdout.write(f"Updated Partner Plan: {partner.setup_fee} setup, {partner.access_fee} access, {partner.monthly_fee}/mo")

        self.stdout.write(self.style.SUCCESS('Done! Pricing plans injected into database.'))
