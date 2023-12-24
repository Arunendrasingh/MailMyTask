import json
import logging
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


# Create your tests here.
logger = logging.getLogger("django")


class TaskPriorityViewsTest(APITestCase):

    test_user_1 = "test_user1@gmail.com"
    test_user_2 = "test_user2@gmail.com"
    test_user_3 = "test_user3@gmail.com"
    test_user_4 = "test_user4@gmail.com"
    test_password = "admin@1234"
    task_priority_url = "/task_priority/"

    # Creating a class fixture to add user in Test DB

    @classmethod
    def setUpClass(cls) -> None:
        """Register 4 User. 3 as SuperAdmin and Staff and one as regular user to test Task Priority."""
        test_user1 = get_user_model().objects.create_superuser(contact=1234567890,
                                                               email=cls.test_user_1, password=cls.test_password)
        test_user1.save()

        test_user2 = get_user_model().objects.create_superuser(contact=1234567890,
                                                               email=cls.test_user_2, password=cls.test_password)
        test_user2.save()

        test_user3 = get_user_model().objects.create_superuser(contact=1234567890,
                                                               email=cls.test_user_3, password=cls.test_password)
        test_user3.save()

        test_user4 = get_user_model().objects.create_user(contact=1234567890,
                                                          email=cls.test_user_4, password=cls.test_password)
        test_user4.is_active = True
        test_user4.save()
        return super().setUpClass()

    def get_auth_token(self, email: str, password: str):
        auth_url = reverse("auth")
        # Authenticate with test_user_1
        response = self.client.post(
            auth_url, data={"email": email, "password": password})

        self.assertEqual(response.status_code, 200)
        return response.json()["access"]

    def test_empty_task_priority(self):
        access_token = self.get_auth_token(
            self.test_user_1, self.test_password)

        response = self.client.get(self.task_priority_url, headers={
                                   'Content-Type': 'application/json', 'Authorization': f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()["resultObject"]), list)
        self.assertEqual(response.json()["resultObject"], [])

    def test_task_priority_with_same_title_and_priority_with_same_user(self):
        """Create two task-priority with test_user_1 with same title. second task-priority must not be created as a task-priority is already available with same title and priority."""

        access_token = self.get_auth_token(
            self.test_user_1, self.test_password)

        request_data = {
            "title": "Priority 1",
            "weight": 1,
            "color": "Orange"
        }
        # Use client to test the Test case. first create a taskpriority with testUser1 and again try to create a task priority with same name for same user and this time code must have to return False.
        response = self.client.post(
            self.task_priority_url, data=request_data, headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 201)
        logger.warning(f"Response is: {response.json()}-at line 77")

        # New Task Priority with same request_data
        response = self.client.post(
            self.task_priority_url, data=request_data, headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 400)
        self.assertNotEqual(response.status_code, 201)
        logger.warning(f"Response is: {response.json()} - at line 84")

    def test_task_priority_with_different_title_and_priority_with_same_user(self):
        """Create a Task priority and after that again create a task priority with same data, and this time API must have to return bad request."""

        access_token = self.get_auth_token(
            self.test_user_1, self.test_password)

        request_data = {
            "title": "Priority 1",
            "weight": 1,
            "color": "Orange"
        }
        response = self.client.post(
            self.task_priority_url, data=request_data, headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 201)
        logger.warning(f"Response is: {response.json()} -at line 100")

        # New Task Priority with same request_data
        request_data = {
            "title": "Priority 2",
            "weight": 2,
            "color": "Orange"
        }
        response = self.client.post(
            self.task_priority_url, data=request_data, headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.status_code, 400)
        logger.warning(f"Response is: {response.json()}-- at line 112")

    def test_different_title_and_priority_with_diff_user(self):
        access_token = self.get_auth_token(
            self.test_user_1, self.test_password)

        request_data = {
            "title": "Priority 1",
            "weight": 1,
            "color": "Orange"
        }
        response = self.client.post(
            self.task_priority_url, data=request_data, headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 201)
        logger.warning(f"Response is: {response.json()} -at line 126")

        # New Task Priority with same request_data
        access_token = self.get_auth_token(
            self.test_user_2, self.test_password)
        request_data = {
            "title": "Priority 1",
            "weight": 1,
            "color": "Orange"
        }
        response = self.client.post(
            self.task_priority_url, data=request_data, headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.status_code, 400)
        logger.warning(f"Response is: {response.json()}-- at line 140")


    def test_only_admin_have_access_to_create_task_priority(self):
        access_token = self.get_auth_token(
            self.test_user_4, self.test_password)
        request_data = {
            "title": "Test Priority One",
            "weight": 5,
            "color": "Orange",
        }
        response = self.client.post(self.task_priority_url, data=request_data, headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 403)

        self.assertNotEqual(response.status_code, 201)
