from rest_framework.test import APITestCase
from django.contrib.auth.models import User


# Create your tests here.

class TaskPriorityViewsTest(APITestCase):

    # Creating a class fixture to add user in Test DB
    @classmethod
    def setUpClass(cls) -> None:
        # Adding Two user with name testUser1 and testUser2 before running test in this class.
        test_user1 = User.objects.create(
            username="testUser1", password="admin@1234")
        test_user1.save()
        test_user2 = User.objects.create(
            username="testUser2", password="admin@1234")
        test_user2.save()
        return super().setUpClass()

    def test_empty_task_priority(self):
        response = self.client.get("/task_priority/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()["resultObject"]), list)
        self.assertEqual(response.json()["resultObject"], [])

    def test_create_new_task_priority_testUser1(self):
        """Create a task priority with testUser1"""

        request_data = {
            "title": "Easy-1",
            "weight": 5,
            "color": "Orange",
            "user": 1
        }
        # Use client to test the Test case. first create a taskpriority with testUser1 and again try to create a task priority with same name for same user and this time code must have to return False.
        response = self.client.post("/task_priority/", data=request_data)
        self.assertEqual(response.status_code, 201)
        # checking response
        self.assertEqual(response.data, {
            "hasError": False,
            "errors": "",
            "resultObject": {
                "id": 1,
                "title": "Easy-1",
                "color": "Orange",
                "weight": 5,
                "user": 1
            }
        })

    def test_title_user_should_unique(self):
        """Create a Task priority and after that again create a task priority with same data, and this time API must have to return bad request."""
        request_data = {
            "title": "Test Priority One",
            "weight": 5,
            "color": "Orange",
            "user": 1
        }
        # Use client to test the Test case. first create a taskpriority with testUser1 and again try to create a task priority with same name for same user and this time code must have to return False.
        response = self.client.post("/task_priority/", data=request_data)
        self.assertEqual(response.status_code, 201)

        request_date_1 = {
            "title": "Test Priority One",
            "weight": 4,
            "color": "Orange",
            "user": 1
        }
        response_1 = self.client.post("/task_priority/", data=request_date_1)
        self.assertNotEqual(response_1.status_code, 201)

    def test_title_dif_user_work(self):
        request_data = {
            "title": "Test Priority One",
            "weight": 5,
            "color": "Orange",
            "user": 1
        }
        # Use client to test the Test case. first create a taskpriority with testUser1 and again try to create a task priority with same name for same user and this time code must have to return False.
        response = self.client.post("/task_priority/", data=request_data)
        self.assertEqual(response.status_code, 201)

        request_date_1 = {
            "title": "Test Priority One",
            "weight": 4,
            "color": "Orange",
            "user": 2
        }
        response_1 = self.client.post("/task_priority/", data=request_date_1)
        self.assertEqual(response_1.status_code, 201)
    
    def test_weight_will_have_to_unique_with_user(self):
        request_data = {
            "title": "Test Priority One",
            "weight": 5,
            "color": "Orange",
            "user": 1
        }
        # Use client to test the Test case. first create a taskpriority with testUser1 and again try to create a task priority with same name for same user and this time code must have to return False.
        response = self.client.post("/task_priority/", data=request_data)
        self.assertEqual(response.status_code, 201)

        request_date_1 = {
            "title": "Test Priority 2",
            "weight": 5,
            "color": "Orange",
            "user": 1
        }
        response_1 = self.client.post("/task_priority/", data=request_date_1)
        self.assertNotEqual(response_1.status_code, 201)



