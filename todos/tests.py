from rest_framework.test import APITestCase
from django.contrib.auth.models import User


# Create your tests here.

class TaskPriorityViewsTest(APITestCase):

    # Creating a class fixture to add user in Test DB
    @classmethod
    def setUpClass(cls) -> None:
        # Adding Two user with name testUser1 and testUser2 before running test in this class.
        test_user1 = User.objects.create(username="testUser1", password="admin@1234")
        test_user1.save()
        test_user2 = User.objects.create(username="testUser2", password="admin@1234")
        test_user2.save()
        return super().setUpClass()

    def test_create_new_priority(self):
        response = self.client.get("/task_priority/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()["resultObject"]), list)
        self.assertEqual(response.json()["resultObject"], [])

    def create_two_new_task_priority_testUser1(APITestCase):
        # TODO: Create new TaskPriority with first user and this should be return as 201
        # TODO: Now Create Priority with same name with same user user na this time request must fail.
        ...

    # TODO: Create a new test function to test teh same with other user and with same priority.

# TODO: Proceed with APIClient.
# TODO: 1-Add test case to add same priority with same user and this test should be failed.
# TODO: 2-Add test case to add same priority with other user and this test have to pass.
# TODO: repeat the test-1 with this user and it should be failed.
