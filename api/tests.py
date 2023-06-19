from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_user_profile_creation(self):
        """Test UserProfile creation"""
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.user, self.user)
        self.assertEqual(str(user_profile), self.user.username)

    def test_user_profile_deletion(self):
        """Test UserProfile deletion"""
        self.user_profile.delete()
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(user=self.user)


class MyAPITestCase(APITestCase):
    """Test case for My API view"""
    def test_my_view(self):
        url = reverse('UserRegistrationView')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {'username': 'admin', 'password': 'admin'}
        self.assertEqual(response.data, expected_data)
