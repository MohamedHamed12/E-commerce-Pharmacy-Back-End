from django.contrib.auth import get_user_model
from django.test import TestCase
from products.models import Wishlist
from rest_framework import status
from rest_framework.test import APIClient

User= get_user_model()
class WishlistViewSetTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create test data
        self.wishlist1 = Wishlist.objects.create(user=self.user, name='Wishlist 1')
        self.wishlist2 = Wishlist.objects.create(user=self.user, name='Wishlist 2')

    def test_get_wishlists(self):
        response = self.client.get('/products/wishlist/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_wishlist(self):
        new_wishlist_data = {
            'user': self.user.id,
            'name': 'New Wishlist',
        }
        response = self.client.post('/products/wishlist/', new_wishlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wishlist.objects.count(), 3)

    def test_get_single_wishlist(self):
        response = self.client.get(f'/products/wishlist/{self.wishlist1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Wishlist 1')

    def test_update_wishlist(self):
        updated_data = {
            'name': 'Updated Wishlist Name',
        }
        response = self.client.patch(f'/products/wishlist/{self.wishlist1.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Wishlist Name')

    def test_delete_wishlist(self):
        response = self.client.delete(f'/products/wishlist/{self.wishlist1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wishlist.objects.count(), 1)

    def test_pagination(self):
        for i in range(10):
            Wishlist.objects.create(user=self.user, name=f'Wishlist {i + 3}')

        response = self.client.get('/products/wishlist/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 12)  # Assuming default pagination limit is 10

    def test_permission_denied(self):
        # Create a new user without admin permissions
        unauthorized_user = User.objects.create_user(username='unauthorized', password='testpassword')
        unauthorized_client = APIClient()
        unauthorized_client.force_authenticate(user=unauthorized_user)

        response = unauthorized_client.get('/products/wishlist/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
