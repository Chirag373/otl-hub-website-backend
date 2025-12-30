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

from api.models import PricingPlan

def get_product_details(signup_data):
    """
    Determine price and product name based on user role or other factors.
    Returns (amount_in_cents, product_name, description)
    """
    role = signup_data.get('role', '').lower()
    
    # Defaults
    price_cents = 0
    product_name = "Account Verification"
    description = "Account Verification Fee"
    
    try:
        plan = PricingPlan.objects.get(plan_type=role)
        
        if role == 'buyer':
            # Subscription/Membership is upfront
            # $120.00 -> 12000 cents
            price_cents = int(plan.buyer_upfront_price * 100)
            product_name = "Buyer Membership"
            description = f"3-Month Membership Commitment (${plan.buyer_monthly_price}/mo billed upfront)"
            
        elif role == 'seller':
            # Setup + Listing Fee
            total = plan.setup_fee + plan.listing_fee
            price_cents = int(total * 100)
            product_name = "Seller Account Setup"
            description = f"Includes ${plan.setup_fee} setup fee + ${plan.listing_fee} listing fee"
            
        elif role == 'realtor':
            # Setup + Access Fee
            total = plan.setup_fee + plan.access_fee
            price_cents = int(total * 100)
            product_name = "Realtor Subscription"
            description = f"Includes ${plan.setup_fee} setup fee + ${plan.access_fee} access fee"
            
        elif role == 'partner':
             # Setup + Access Fee
            total = plan.setup_fee + plan.access_fee
            price_cents = int(total * 100)
            product_name = "Partner Subscription"
            description = f"Includes ${plan.setup_fee} setup fee + ${plan.access_fee} access fee"
            
    except PricingPlan.DoesNotExist:
        # Fallback to hardcoded if no DB entry found
        if role == 'buyer':
            return 12000, "Buyer Membership", "3-Month Membership Commitment ($40/mo billed upfront)"
        elif role == 'seller':
            return 29800, "Seller Account Setup", "Includes $99 setup fee + $199 listing fee"
        elif role == 'realtor':
             return 19800, "Realtor Subscription", "Includes $99 setup fee + $99 access fee"
        elif role == 'partner':
             return 49800, "Partner Subscription", "Includes $199 setup fee + $299 access fee"
        return 1000, "Account Verification Fee", "Standard verification fee"

    return price_cents, product_name, description

# Keep the old function signature for backward compatibility just in case, or alias it
def get_price_for_user(signup_data):
    amount, _, _ = get_product_details(signup_data)
    return amount

class CreateAccessPassSessionView(APIView):
    """
    Create a Stripe Checkout Session for Buyer Access Pass
    """
    def post(self, request):
        if not request.user.is_authenticated or request.user.role != 'BUYER':
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            # Determine price from PricingPlan
            try:
                from api.models import PricingPlan
                plan = PricingPlan.objects.get(plan_type='buyer')
                price_amount = int(plan.buyer_access_pass_price * 100)
            except (PricingPlan.DoesNotExist, ImportError):
                price_amount = 65000 # Fallback

            product_name = "Buyer Access Pass"
            description = "30-Day Access Pass to unlock seller contacts"
            
            success_url = request.build_absolute_uri(reverse('access-pass-success')) + "?session_id={CHECKOUT_SESSION_ID}"
            cancel_url = request.build_absolute_uri('/buyer/dashboard')
            
            # Prepare session arguments
            session_kwargs = {
                'payment_method_types': ['card'],
                'line_items': [{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product_name,
                            'description': description,
                        },
                        'unit_amount': price_amount,
                    },
                    'quantity': 1,
                }],
                'mode': 'payment',
                'invoice_creation': {"enabled": True},
                'success_url': success_url,
                'cancel_url': cancel_url,
                'client_reference_id': str(request.user.id),
                'metadata': {
                    'type': 'access_pass',
                    'user_id': str(request.user.id)
                }
            }
            
            # Start logic: Either 'customer' OR 'customer_email'
            if request.user.stripe_customer_id:
                session_kwargs['customer'] = request.user.stripe_customer_id
            else:
                session_kwargs['customer_email'] = request.user.email
                session_kwargs['customer_creation'] = 'always' # Create a customer if one doesn't exist
            
            checkout_session = stripe.checkout.Session.create(**session_kwargs)
            return Response({'url': checkout_session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AccessPassSuccessView(APIView):
    """
    Handle successful Access Pass payment
    """
    permission_classes = [] # Allow callback to hit this, but we'll verify session
    
    def get(self, request):
        session_id = request.GET.get('session_id')
        if not session_id:
            return Response({'error': 'No session_id provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except stripe.error.StripeError as e:
             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
             
        if session.payment_status == 'paid':
             # Verify it's an Access Pass session
             if session.metadata.get('type') == 'access_pass':
                 user_id = session.metadata.get('user_id')
                 try:
                     from core.models import User
                     from api.models import BuyerProfile
                     from django.utils import timezone
                     from datetime import timedelta
                     
                     user = User.objects.get(id=user_id)
                     profile = BuyerProfile.objects.get(user=user)
                     
                     # 1. Update Expiry Date
                     # If already active, add 30 days to existing expiry? 
                     # Or just set to now + 30 days? 
                     # Requirement: "Extensions ... +15 days". But this is a new pass purchase ($650).
                     # "Valid for 30 days".
                     # "Buyer cannot unlock new seller contacts without buying another Access Pass" -> Implies strictly specific durations.
                     # Let's add 30 days from NOW, or extend if currently active.
                     
                     now = timezone.now()
                     if profile.access_pass_expiry and profile.access_pass_expiry > now:
                         profile.access_pass_expiry += timedelta(days=30)
                     else:
                         profile.access_pass_expiry = now + timedelta(days=30)
                         
                     profile.save()
                     
                     return redirect('/buyer/dashboard?success=access_pass_activated')
                     
                 except Exception as e:
                     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return redirect('/buyer/dashboard?error=payment_failed')


class PaymentSuccessView(APIView):
    """
    Handle successful payment
    """
    permission_classes = []

    def get(self, request):
        session_id = request.GET.get('session_id')
        print(f"DEBUG: PaymentSuccessView called with session_id: {session_id}")
        
        if not session_id:
            return Response({'error': 'No session_id provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            print(f"DEBUG: Stripe Session Status: {session.payment_status}")
            print(f"DEBUG: Session Client Ref ID: {session.client_reference_id}")
            print(f"DEBUG: Session Email: {session.customer_email}")
            
        except stripe.error.StripeError as e:
            print(f"DEBUG: Stripe Error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if session.payment_status == 'paid':
            # Retrieve PendingSignup
            try:
                # We stored pending_signup_id in client_reference_id
                pending_signup_id = session.client_reference_id
                pending_signup = PendingSignup.objects.get(id=pending_signup_id)
                signup_data = pending_signup.signup_data
                
                print(f"DEBUG: Found PendingSignup: {pending_signup.email}")
                
                # Create the user
                serializer = SignupSerializer(data=signup_data)
                if serializer.is_valid(raise_exception=True):
                    user = serializer.save()
                    user.is_active = True
                    
                    # Store Stripe Customer ID
                    if session.customer:
                        user.stripe_customer_id = session.customer
                        
                    user.save()
                    print(f"DEBUG: User created successfully: {user.email}")
                    
                    # Delete pending signup
                    pending_signup.delete()
                    
                    # Redirect to Login Page
                    # Use reverse to ensure correct URL construction
                    login_url = reverse('login')
                    return redirect(f"{login_url}?success=account_created")
                    
            except PendingSignup.DoesNotExist:
                 print(f"DEBUG: PendingSignup {session.client_reference_id} not found.")
                 # Check if user already exists (maybe page refresh?)
                 email = session.customer_email or session.metadata.get('email')
                 if email:
                     from core.models import User
                     if User.objects.filter(email=email).exists():
                         print(f"DEBUG: User {email} already exists. Redirecting to login.")
                         login_url = reverse('login')
                         return redirect(f"{login_url}?success=account_created")
                 
                 return Response({'error': 'Signup data not found or already processed.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(f"DEBUG: Exception in PaymentSuccessView: {str(e)}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        print(f"DEBUG: Payment status not 'paid': {session.payment_status}")
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
