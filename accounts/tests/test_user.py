import email
import profile
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC, EmailAddress
from django.core import mail
import re
#user serializer

from dj_rest_auth.serializers import UserDetailsSerializer
from accounts.models import EmailVerificationOTP, Profile
User = get_user_model()
class UserTest(APITestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'test@example.com',
            "first_name": "test",
            "last_name": "test",
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'gender': 'male'
        }
    def test_registration(self):
        url = reverse('rest_register')
        
        response = self.client.post(url, self.data)
        # get user
        user = User.objects.get(email=self.data['email'])
        # ser=UserDetailsSerializer(user)
        # print(ser.data )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_not_created_profile(self):
        self.test_registration()

        profile = Profile.objects.get(user__email=self.data['email'])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(profile.user.email, self.data['email'])
        # self.assertEqual(User.objects.count(), 1)
        # self.assertEqual(User.objects.get().email, 'test@example.com')
   
    def test_login_unconfirmed_email(self):
        url = reverse('rest_login')
        response=self.client.post(url,{   'email': 'test@example.com',  'password': 'testpassword'})
        self.assertEqual(response.status_code,400)

    def test_email_confirmation(self):
        self.test_registration()
        st=mail.outbox[-1].body.find(":")+1
        otp=mail.outbox[-1].body[st:].strip()
        url=reverse('verify-email-otp' )
        response=self.client.post(url ,{'otp':otp})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access=response.data['access']
        url=reverse('token_verify')
        response=self.client.post(url,{'token':access})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    def test_login_confirmed_email(self):
        self.test_email_confirmation()
        url = reverse('rest_login')
        response=self.client.post(url,{   'email': 'test@example.com',  'password': 'testpassword'})
        self.assertEqual(response.status_code,200)
        # login with username 
        url = reverse('rest_login')
        response=self.client.post(url,{   'username': 'testuser',  'password': 'testpassword'})
        self.assertEqual(response.status_code,200)

    
    def test_otp_by_email(self):
        self.test_login_confirmed_email()
        url = reverse('otp-by-email')
        response=self.client.post(url,{   'email': 'test@example.com'})
      
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_data(self):
        self.test_otp_by_email()
        # user and token
        user=User.objects.get(email=self.data['email'])
        # access token
        url = reverse('rest_login')
        response=self.client.post(url,{   'email': 'test@example.com',  'password': 'testpassword'})
        # print(response.data)
        access_token=response.data['access']
        url=reverse('rest_user_details')
        response=self.client.get(url,HTTP_AUTHORIZATION=f'Bearer {access_token}')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_check_email(self):
        self.test_user_data()
        url = reverse('check-email')
        response=self.client.post(url,{   'email': 'test@example.com'})
      
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response=self.client.post(url,{   'email': 'test2@example.com'})
  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_username(self):
        self.test_user_data()
        url = reverse('check-username')
        response=self.client.post(url,{   'username': 'testuser'})
      
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response=self.client.post(url,{   'username': 'test2user'})
  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# rest password otp

class PasswordResetTests(APITestCase):
    def setUp(self) :
        url=reverse('rest_register')
        self.data={
            'email': 'test@example.com',
            "first_name": "test",
            "last_name": "test",
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'gender': 'male'
        }
        self.client.post(url,self.data)
        st=mail.outbox[-1].body.find(":")+1
        otp=mail.outbox[-1].body[st:].strip()
        url=reverse('verify-email-otp' )
        response=self.client.post(url ,{'otp':otp})
        self.access=response.data['access']
        # self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        self.user=User.objects.get(email='test@example.com')  

    def test_otp_by_email(self):
        url = reverse('otp-by-email')
        response=self.client.post(url,{   'email': 'test@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_reseve_otp(self):
        url = reverse('otp-by-email')
        response=self.client.post(url,{   'email': 'test@example.com'})
        st=mail.outbox[-1].body.find(":")+1
        otp=mail.outbox[-1].body[st:].strip()
        url=reverse('verify-email-otp' )
        response=self.client.post(url ,{'otp':otp})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_change_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        url = reverse('rest_password_change')
        response=self.client.post(url ,{'old_password': 'testpassword','new_password1': 'testpassword1','new_password2': 'testpassword1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        
# # reset password link
# # class PasswordResetTests(APITestCase):
# #     def test_password_reset_request(self):
# #         user = User.objects.create_user(username='testuser',email='test@example.com', password='testpassword')
# #         url = reverse('rest_password_reset')
# #         data = {'email': 'test@example.com'}
# #         response = self.client.post(url, data)
# #         # print(response.status_code)
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         self.assertEqual(len(mail.outbox), 1)
# #         # print(mail.outbox[0].body)
# #         # self.assertEqual(mail.outbox[0].subject, 'Password reset on example.com')

# #     def test_password_reset_confirm(self):
# #         # Create a user object
# #         user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

      
# #         response = self.client.post(reverse('rest_password_reset'),  {'email': 'test@example.com'})
# #         # print(mail.outbox[0].body)
# #         st=mail.outbox[0].body.find('http')
# #         link = mail.outbox[0].body[st:]
# #         link=link[:link.find('\n')]
# #         pattern = r'http://testserver/accounts/rest-auth/password/reset/confirm/(?P<uid>[\w-]+)/(?P<token>[\w-]+)'

# #         match = re.search(pattern, link)


# #         uid = match.group('uid')
# #         token = match.group('token')
# #         # print(uid,token)
       
# #         data = {
# #             'uid': uid,
# #             'token': token,
# #             'new_password1': 'newpassword',
# #             'new_password2': 'newpassword',
# #         }

# #         # Make the POST request to the password reset confirmation URL
# #         url = reverse('rest_password_reset_confirm')
# #         response = self.client.post(url, data)
# #         # print(response.data)
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         self.assertEqual(response.data['detail'], 'Password has been reset with the new password.')

#     # def test_password_change(self):
#     #     user = User.objects.create_user(username='testuser',email='test@example.com', password='testpassword')
#     #     self.client.force_authenticate(user=user)
#     #     url = reverse('rest_password_change')
#     #     data = {
#     #         'old_password': 'testpassword',
#     #         'new_password1': 'newpassword',
#     #         'new_password2': 'newpassword',
#     #     }
#     #     response = self.client.post(url, data)
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(response.data['detail'], 'New password has been saved.')


# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.contrib.auth.models import User

class CheckPasswordViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',email='test@example.com', password='test_password')
        self.client.force_authenticate(user=self.user)

    def test_check_valid_password(self):
        url = reverse('check-password')  # Assuming you've named your URL pattern 'check-password'
        data = {'password': 'test_password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['detail'], 'Password is valid')

    def test_check_invalid_password(self):
        url = reverse('check-password')  # Assuming you've named your URL pattern 'check-password'
        data = {'password': 'wrong_password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.data['detail'], 'Password is invalid')
