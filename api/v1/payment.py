from django.conf import settings
from django.shortcuts import redirect
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from core.models import PendingSignup
from api.v1.serializer import SignupSerializer
from django.contrib.auth import login

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_product_details(signup_data):
    """
    Determine price and product name based on user role or other factors.
    Returns (amount_in_cents, product_name, description)
    """
    role = signup_data.get('role')
    
    if role == 'BUYER':
        # Buyer Pricing
        plan = signup_data.get('selected_plan')
        if plan == 'basic':
            return 12400, "Buyer Basic Plan", "Includes $99 setup fee + $25 basic plan"
        else:
            return 14900, "Buyer Pro Plan", "Includes $99 setup fee + $50 pro plan"
            
    elif role == 'SELLER':
        # Seller Pricing
        return 29800, "Seller Account Setup", "Includes $99 setup fee + $199 listing fee"
        
    elif role == 'REALTOR':
        # Realtor Pricing
        return 19800, "Realtor Subscription", "Includes $99 setup fee + $99 access fee"
        
    elif role == 'PARTNER':
        # Partner Pricing
        return 49800, "Partner Subscription", "Includes $199 setup fee + $299 access fee"
        
    return 1000, "Account Verification Fee", "Standard verification fee"

# Keep the old function signature for backward compatibility just in case, or alias it
def get_price_for_user(signup_data):
    amount, _, _ = get_product_details(signup_data)
    return amount

class PaymentSuccessView(APIView):
    """
    Handle successful payment
    """
    permission_classes = []

    def get(self, request):
        session_id = request.GET.get('session_id')
        if not session_id:
            return Response({'error': 'No session_id provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if session.payment_status == 'paid':
            # Retrieve PendingSignup
            try:
                # We stored pending_signup_id in client_reference_id
                pending_signup_id = session.client_reference_id
                pending_signup = PendingSignup.objects.get(id=pending_signup_id)
                signup_data = pending_signup.signup_data
                
                # Create the user
                serializer = SignupSerializer(data=signup_data)
                if serializer.is_valid(raise_exception=True):
                    user = serializer.save()
                    user.is_active = True
                    
                    # Store Stripe Customer ID
                    if session.customer:
                        user.stripe_customer_id = session.customer
                        
                    user.save()
                    
                    # Delete pending signup
                    pending_signup.delete()
                    
                    # Redirect to Login Page
                    # The user requested "redirect me to the login page"
                    return redirect('/login?success=account_created')
                    
            except PendingSignup.DoesNotExist:
                 return Response({'error': 'Signup data not found or already processed.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': 'Payment not completed.'}, status=status.HTTP_400_BAD_REQUEST)

class BillingPortalView(APIView):
    """
    Redirects to Stripe Customer Portal
    """
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login')
            
        if not request.user.stripe_customer_id:
            # If no customer ID, maybe just redirect to dashboard or show message
            # For now, simplistic approach:
             return Response({'error': 'No billing account found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Determine return URL based on User Role to go back to dashboard
            return_path = '/'
            if request.user.role == 'BUYER': return_path = '/buyer/dashboard'
            elif request.user.role == 'SELLER': return_path = '/seller/dashboard'
            elif request.user.role == 'REALTOR': return_path = '/realtor/dashboard'
            elif request.user.role == 'PARTNER': return_path = '/partner/dashboard'

            portal_session = stripe.billing_portal.Session.create(
                customer=request.user.stripe_customer_id,
                return_url=request.build_absolute_uri(return_path) 
            )
            return redirect(portal_session.url)
        except Exception as e:
             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def create_checkout_session(request, pending_signup):
    """
    Create a Stripe Checkout Session for the pending verification
    """
    try:
        price_amount, product_name, description = get_product_details(pending_signup.signup_data)
        success_url = request.build_absolute_uri(reverse('payment-success')) + "?session_id={CHECKOUT_SESSION_ID}"
        # Cancel URL should point to frontend signup page, not API
        cancel_url = request.build_absolute_uri('/signup') 

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=pending_signup.email, # USE THE SIGNUP EMAIL
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product_name,
                        'description': description, # Optional description
                    },
                    'unit_amount': price_amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            locale='en', # Attempt to default to English/US context
            customer_creation='always',
            invoice_creation={"enabled": True}, 
            payment_intent_data={'setup_future_usage': 'on_session'},
            success_url=success_url,
            cancel_url=cancel_url,
            client_reference_id=str(pending_signup.id),
            metadata={
                'email': pending_signup.email,
                'role': pending_signup.signup_data.get('role', '')
            }
        )
        return checkout_session.url
    except Exception as e:
        raise e
