# -*- coding: utf-8 -*-

from accounts.models import *
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User=get_user_model()
# testcase

# testcase


class PatientTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "test",
            "last_name": "test",
            "gender": "male",
        }
        self.patient_data = {
            "first_name": "John",
            "last_name": "Doe",
            "bio": "This is a test bio.",
            "date_of_birth": "1990-01-01",
            "gender": "Male",
        }

        # Create a user and obtain a token for authentication
        url = reverse("rest_register")
        self.client.post(url, self.user_data, format="json")
        # confirm email


        st = mail.outbox[-1].body.find(":") + 1
        otp = mail.outbox[-1].body[st:].strip()
        url = reverse("verify-email-otp")
        self.client.post(url, {"otp": otp})
        # print(response)

        self.user = User.objects.get(email=self.user_data["email"])
        # self.user = User.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        # patient_id=self.user.patient.id
        # print("hhh")
        # print(patient_id)
        # Set the Authorization header with the token
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_update_user_patient_without_token(self):
        # pass
        url = reverse(
            "patient-detail", args=[self.user.patient.id]
        )  # Assuming 'patient-detail' is the name generated by the router
        self.patient_data["user"] = self.user.id
        response = self.client.put(url, self.patient_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def teste_update_user_patient_with_invalid_token(self):
        url = reverse(
            "patient-detail", args=[self.user.patient.id]
        )  # Assuming 'patient-detail' is the name generated by the router
        self.patient_data["user"] = self.user.id
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}invalid")
        response = self.client.put(url, self.patient_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_patient(self):
        url = f"/accounts/patient/{self.user.patient.id}/"

        # self.patient_data["user"] = self.user.id

        # Set the Authorization header with the token
        access=RefreshToken.for_user(self.user).access_token

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        response = self.client.patch(url, {"first_name": "New First Name"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_updata_image(self):
        url = reverse(
            "patient-detail", args=[self.user.patient.id]
        )  # Assuming 'patient-detail' is the name generated by the router
        self.patient_data["user"] = self.user.id
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.put(url, self.patient_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)



#     def test_update_user_patient_without_patient(self):
#         url = reverse(
#             "patient-detail", args=["1000"]
#         )  # Assuming 'patient-detail' is the name generated by the router
#         self.patient_data["user"] = self.user.id
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
#         response = self.client.put(url, self.patient_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_user_patient_without_user(self):
#         url = reverse(
#             "patient-detail", args=[self.user.patient.id]
#         )  # Assuming 'patient-detail' is the name generated by the router
#         uuid_example = uuid.uuid4()
#         self.patient_data["user"] = uuid_example
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
#         response = self.client.put(url, self.patient_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_delete_user_patient(self):
#         url = reverse(
#             "patient-detail", args=[self.user.patient.id]
#         )  # Assuming 'patient-detail' is the name generated by the router
#         self.patient_data["user"] = self.user.id
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_get_user_patient(self):
#         url = reverse(
#             "patient-detail", args=[self.user.patient.id]
#         )  # Assuming 'patient-detail' is the name generated by the router
#         self.patient_data["user"] = self.user.id
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_user_patients(self):
#         url = reverse("patient-list")
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_filters_by_user_id(self):
#         url = reverse("rest_register")
#         for i in range(30):
#             self.client.post(url, self.user_data, format="json")

#         url = "/accounts/patient/"
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
#         response = self.client.get(url, {"user__id": self.user.id})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         uuid_example="00000000-0000-0000-0000-000000000000"
#         response = self.client.get(url, {"user__id": uuid_example})
#         # print(response.data,response.status_code)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 0)



# class MockingProfileTest(APITestCase):
#     def setUp(self):
#         self.user_data = {
#             "username": "testuser",
#             "email": "test@example.com",
#             "password1": "testpassword",
#             "password2": "testpassword",
#             "first_name": "test",
#             "last_name": "test",
#             "gender": "male",
#         }
#         self.patient_data = {
#             "first_name": "John",
#             "last_name": "Doe",
#             "bio": "This is a test bio.",
#             "date_of_birth": "1990-01-01",
#             "gender": "Male",
#         }

#         url = reverse("rest_register")
#         self.client.post(url, self.user_data, format="json")

#         self.user = User.objects.get(email=self.user_data["email"])
#         refresh = RefreshToken.for_user(self.user)
#         self.access_token = str(refresh.access_token)
#         self.image = (
#             b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
#             b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
#             b"\x02\x4c\x01\x00\x3b"
#         )

#     @patch("django.core.files.storage.FileSystemStorage._save")
#     def test_serializer_contains_expected_fields(
#         self,
#         mock_save,
#     ):
#         mock_save.return_value = (
#             "test_patient.jpg"  # Mocking the save method to return the expected value
#         )

#         updated_data = {
#             "patient_image": SimpleUploadedFile(
#                 name="test_patient.jpg",
#                 content=b"mock image data",
#                 content_type="image/jpeg",
#             )
#         }

#         # Assuming self.client is an instance of APIClient
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
#         url = reverse(
#             "patient-detail", args=[self.user.patient.id]
#         )  # Assuming 'patient-detail' is the name generated by the router
#         response = self.client.patch(url, updated_data, format="multipart")

#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         response_patient = self.client.get(url).data
#         self.user.patient.image = "default/user.jpg"
#         self.assertEqual(self.user.patient.image, "default/user.jpg")
#         data = {"image": None}
#         response = self.client.patch(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response_patient["image"], "media/default/user.jpg")
#         # self.assertTrue(
#         #     os.path.exists(os.path.join(settings.MEDIA_ROOT, "default/user.jpg"))
#         # )
