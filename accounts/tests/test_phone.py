import email
from os import access
from urllib import response
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import PhoneModel  # Update with the correct import
from django.core import mail
from django.contrib.auth import get_user_model
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC, EmailAddress

from accounts.tests.test_user import UserTest 
User=get_user_model()


class GetPhoneNumberRegisteredTimeBasedTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.phone_number = "1234567890"  # Replace with a phone number you want to use
        user = User.objects.create_user(username='testuser',email='test@example.com', password='testpassword')
        # get access token
        response = self.client.post(reverse('rest_login'), {'email': 'test@example.com', 'password': 'testpassword'})
        self.access = response.data['access']
        # self.client.force_authenticate(user=user)


    def test_register_phone_number_not_auth(self):
        response = self.client.post(reverse('phone-register'), {"phone": self.phone_number})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_phone_number(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        response = self.client.post(reverse('phone-register'), {"phone": self.phone_number})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(PhoneModel.objects.filter(Mobile=self.phone_number).exists())

    def test_get_request_returns_otp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        response = self.client.post(reverse('phone-register'), {"phone": self.phone_number})
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("OTP" , response.data)

    def test_post_request_with_valid_otp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        response = self.client.post(reverse('phone-register'), {"phone": self.phone_number})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        otp=response.data["OTP"]
        response = self.client.post(reverse('verify-mobile-otp'), {"otp": otp, "phone": self.phone_number})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mobile = PhoneModel.objects.get(Mobile=self.phone_number)
        self.assertTrue(mobile.isVerified)


    def test_post_request_with_invalid_otp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        PhoneModel.objects.create(Mobile=self.phone_number)
        otp = "000000"  # Replace with an invalid OTP
        response = self.client.post(reverse('verify-mobile-otp'), {"otp": otp, "phone": self.phone_number})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_nonexistent_phone_number(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        response = self.client.post(reverse('verify-mobile-otp'), {"otp": "123456", "phone": "9999999999"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_request_with_verified_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        PhoneModel.objects.create(Mobile=self.phone_number, isVerified=True)
        otp = "123456"  
        response = self.client.post(reverse('verify-mobile-otp'), {"otp": otp, "phone": self.phone_number})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
