from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

# Create your tests here.


class UserManagerTest(APITestCase):
    def test_create_user(self):
        User = get_user_model()

        user = User.objects.create_user(
            email="test@gmail.com", contact=1234567890, password="1234")

        self.assertEqual(user.email, "test@gmail.com")
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_user()

        with self.assertRaises(TypeError):
            User.objects.create_user(password=123456789)

        with self.assertRaises(ValueError):
            User.objects.create_user(email = "", contact="", password="")

    
    def test_create_super_user(self):
        User = get_user_model()

        user = User.objects.create_superuser(
            email="test@gmail.com", contact=1234567890, password="1234")

        self.assertEqual(user.email, "test@gmail.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_superuser()

        with self.assertRaises(TypeError):
            User.objects.create_superuser(password=123456789)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email = "", contact="", password="")

