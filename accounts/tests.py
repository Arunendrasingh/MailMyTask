import json
from rest_framework import status
from django.urls import include, reverse, path
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.contrib.auth import get_user_model

# Create your tests here.


class UserManagerTest(APITestCase):
    def test_create_user(self):
        user_model = get_user_model()

        user = user_model.objects.create_user(
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
            user_model.objects.create_user()

        with self.assertRaises(TypeError):
            user_model.objects.create_user(password=123456789)

        with self.assertRaises(ValueError):
            user_model.objects.create_user(email="", contact="", password="")

    def test_create_super_user(self):
        user_model = get_user_model()

        user = user_model.objects.create_superuser(
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
            user_model.objects.create_superuser()

        with self.assertRaises(TypeError):
            user_model.objects.create_superuser(password=123456789)

        with self.assertRaises(ValueError):
            user_model.objects.create_superuser(email="", contact="", password="")


class UserLoginTest(APITestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # Adding Two user with name testUser1 and testUser2 before running test in this class.
        user = get_user_model()
        test_user1 = user.objects.create_user(
            email="testUser1@gmail.com", contact=1234567890, password="admin@1234")
        test_user1.is_active = True
        test_user1.save()
        test_user2 = user.objects.create_user(
            email="testUser2@gmail.com", contact=1234567890, password="admin@1234")
        test_user2.save()
        return super().setUpClass()

    def test_user_login(self):
        request_data = {
            "email": "testUser1@gmail.com",
            "password": "admin@1234"
        }
        url = reverse("auth")
        response = self.client.post(url, data=request_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([key for key in response.json().keys()], ["refresh", "access"])
        self.assertEqual(response.status_code, 200)

    def test_incorrect_user_credentials(self):
        "Test a user must not be authenticated with wrong credentials."
        request_data = {
            "email": "testUser1@gmail.com",
            "password": "admin@"
        }

        url = reverse("auth")
        response = self.client.post(url, data=request_data)

        self.assertEqual(response.status_code, 401)

    def test_in_active_user_must_not_login(self):
        "Test a user must not be authenticated with wrong credentials."
        request_data = {
            "email": "testUser2@gmail.com",
            "password": "admin@1234"
        }

        url = reverse("auth")
        response = self.client.post(url, data=request_data)

        self.assertEqual(response.status_code, 401)
