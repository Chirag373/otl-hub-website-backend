import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import User

def generate_otp(length=8):
    """Generate a numeric OTP of given length."""
    return ''.join(random.choices(string.digits, k=length))

def send_verification_email(email, otp):
    """
    Send OTP email to a specific address without User dependency.
    """
    try:
        subject = 'Verify your email - OTL Platform'
        message = f'Your verification code is: {otp}\n\nPlease enter this code to verify your account.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_otp_email(user_email):
    """
    Generate OTP, save to user, and send email.
    Returns True if successful, False otherwise.
    """
    try:
        user = User.objects.get(email=user_email)
        otp = generate_otp()
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        return send_verification_email(user_email, otp)
    except User.DoesNotExist:
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
