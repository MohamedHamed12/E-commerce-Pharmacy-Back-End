# -*- coding: utf-8 -*-
import pyotp
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from PIL import Image

from .models import EmailVerificationOTP

User = get_user_model()

def create_image():
    """Create a blank 200x200 white RGB image."""
    return Image.new("RGB", (200, 200), color=(255, 255, 255))

class OtpService:
    """Handles OTP generation and verification."""

    @staticmethod
    def generate_otp():
        """Generates an OTP and the corresponding secret key."""
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret, interval=120)
        return {"totp": secret, "OTP": totp.now()}

    @staticmethod
    def verify_otp(otp):
        """Verifies if the provided OTP is valid."""
        try:
            email_verification = EmailVerificationOTP.objects.get(otp=otp)
        except ObjectDoesNotExist:
            return None

        # Verify OTP
        totp = pyotp.TOTP(email_verification.activation_key, interval=120)
        if not totp.verify(otp):
            return None

        # Mark email as verified
        email_address = EmailAddress.objects.filter(user=email_verification.user).first()
        if email_address:
            email_address.verified = True
            email_address.save()

        # Clean up verification entry
        email_verification.delete()
        return email_verification.user

class EmailService:
    """Handles sending emails, such as OTP emails."""

    @staticmethod
    def send_otp_email(user):
        """Sends an OTP email to the given user."""
        otp_data = OtpService.generate_otp()
        otp = otp_data["OTP"]
        activation_key = otp_data["totp"]

        # Save or update OTP for the user
        email_verification, created = EmailVerificationOTP.objects.update_or_create(
            user=user, defaults={"otp": otp, "activation_key": activation_key}
        )

        # Send the OTP email
        subject = "Your OTP Code"
        body = f"Your OTP is: {otp}"
        send_mail(subject, body, "your_email@gmail.com", [user.email])
