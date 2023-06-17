from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

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
