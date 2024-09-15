# -*- coding: utf-8 -*-
from accounts.filters import *
from accounts.models import *
from accounts.serializers import *
from accounts.utils import *
from allauth.socialaccount import signals
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.facebook.views import \
    FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from dj_rest_auth.views import LoginView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegistration

    # permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer=CustomRegistration(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        response  = super().post(request, *args, **kwargs)
        user = User.objects.get(id=response.data['user']['pk'])

        if 'user_type' in serializer.data:
            user.user_type=serializer.data['user_type']
            user.save()

        POSITIONS[user.user_type].objects.create(
            user=user,
            first_name=serializer.data['first_name'],
            last_name = serializer.data["last_name"]   ,
            gender = serializer.data["gender"] )



        EmailService.send_otp_email(user)
        return Response({"detail": "Verify your email"}, status=status.HTTP_201_CREATED)


# check if email exists and verified
class UnlinkProviderView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UnlinkProviderSerializer

    def post(self, request, *args, **kwargs):
        serializer = UnlinkProviderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.validated_data["provider"]
        user = User.objects.get(email=serializer.validated_data["email"])
        social_account = SocialAccount.objects.get(user=user, provider=provider)

        if social_account:
            # send unlink to provider

            social_account.delete()
            signals.social_account_removed.send(
                sender=SocialAccount, request=self.request, socialaccount=social_account
            )
            return Response(
                {"detail": "Provider unlinked successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Provider not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CustomTokenObtainPairView(LoginView):
    def post(self, request, *args, **kwargs):
        response= super().post(request, *args, **kwargs)

        if not (self.user.is_superuser or self.user.is_staff or  EmailAddress.objects.filter(user=self.user,
                                        verified=True).exists()):
            return  Response({'error': 'Email address not verified.'}, status=400)

        response.data['user']=CustomUserSerializer(self.user).data
        try:
            response.data['profile_id']=POSITIONS[self.user.user_type].objects.get(user=self.user).id
        except ObjectDoesNotExist:
            response.data['profile_id']=None
            pass
        return response

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter







# class GoogleLogin(
#     SocialLoginView
# ):  # if you want to use Authorization Code Grant, use this
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = "http://localhost:3000"
#     client_class = OAuth2Client
class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:8000/accounts/google/login/callback/'  # Replace with your callback URI
    client_class = OAuth2Client
    def post(self, request, *args, **kwargs):

        response= super().post(request, *args, **kwargs)




        user = User.objects.get(id=response.data['user']['pk'])

        try:

            Patient.objects.create(
                user=user)
        except Exception:
            pass

        response.data['user']=CustomUserSerializer(self.user).data

        try:
            response.data['profile_id']=Patient.objects.get(user=self.user).id
        except ObjectDoesNotExist:
            response.data['profile_id']=None
            pass
        print(response.data)
        return response
