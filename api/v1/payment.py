import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

stripe.api_key = settings.STRIPE_SECRET_KEY

# Configuration: Centralize prices and logic here
# In a large app, move this to a separate utility file or settings.py
PRICING_CONFIG = {
    'BUYER': {
        'mode': 'payment',
        'setup_fee': 9900,
        'plans': {
            'basic': {'amount': 2500, 'name': 'Buyer Basic Plan (3 Months)'},
            'pro':   {'amount': 5000, 'name': 'Buyer Pro Plan (6 Months)'},
        }
    },
    'REALTOR': {
        'mode': 'subscription',
        'setup_fee': 9900,
        'plans': {
            'default': {'amount': 4900, 'name': 'Realtor Professional Subscription', 'interval': 'month'}
        }
    },
    'PARTNER': {
        'mode': 'subscription',
        'setup_fee': 19900,
        'plans': {
            'default': {'amount': 9900, 'name': 'Partner Business Subscription', 'interval': 'month'}
        }
    },
    'SELLER': {
        'mode': 'payment',
        'setup_fee': 0, # Listing fee acts as the main price
        'plans': {
            'default': {'amount': 29800, 'name': 'Seller Property Listing Plan'}
        }
    }
}

class CreateStripeCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def _build_line_items(self, role, plan_name):
        """Helper to construct line items based on configuration."""
        config = PRICING_CONFIG.get(role)
        if not config:
            raise ValueError("Invalid User Role")

        # Determine specific plan details
        # If role has only one plan (like Seller/Realtor), default to it
        plan_details = config['plans'].get(plan_name) or config['plans'].get('default')
        
        if not plan_details:
            raise ValueError("Invalid Plan Name")

        line_items = []

        # 1. Add Setup Fee (if applicable)
        if config['setup_fee'] > 0:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f'{role.title()} Account Setup Fee'},
                    'unit_amount': config['setup_fee'],
                },
                'quantity': 1,
            })

        # 2. Add Main Plan (Subscription or One-time)
        price_data = {
            'currency': 'usd',
            'product_data': {'name': plan_details['name']},
            'unit_amount': plan_details['amount'],
        }

        # Add recurring interval if it exists in config
        if 'interval' in plan_details:
            price_data['recurring'] = {'interval': plan_details['interval']}

        line_items.append({
            'price_data': price_data,
            'quantity': 1,
        })

        return line_items, config['mode']

    def post(self, request):
        user = request.user
        role = getattr(user, 'role', None) # Safely get role
        plan_name = request.data.get('plan_name', 'basic') # Default to basic
        
        # 1. Validation & Logic Construction
        try:
            line_items, mode = self._build_line_items(role, plan_name)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Determine Domain (Best practice: Use settings, fall back to request)
        domain = getattr(settings, 'FRONTEND_URL', f"{request.scheme}://{request.get_host()}")

        # 3. Customer Handling
        # If your User model saves the stripe_id, use it. Otherwise use email.
        customer_kwargs = {}
        if hasattr(user, 'stripe_customer_id') and user.stripe_customer_id:
            customer_kwargs['customer'] = user.stripe_customer_id
        else:
            customer_kwargs['customer_email'] = user.email
            # Optional: Ensure a new customer is created if you want to save it later via webhook
            customer_kwargs['customer_creation'] = 'if_required' 

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode=mode,
                success_url=f"{domain}/login?message=payment-success&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{domain}/signup",
                metadata={
                    'user_id': user.id,
                    'role': role,
                    'plan_name': plan_name
                },
                allow_promotion_codes=True, # Highly recommended for flexibility
                **customer_kwargs
            )
            return Response({'url': checkout_session.url})

        except stripe.error.StripeError as e:
            # Handle specific Stripe API errors
            return Response({'error': e.user_message or "Payment service error"}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            # Handle internal errors
            return Response({'error': "An internal error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)