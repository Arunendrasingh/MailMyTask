import copy
from django.urls import include, reverse, path
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

# Create your tests here.


class UserManagerTest(APITestCase):
    def test_create_user(self):
        user_model = get_user_model()

        user = user_model.objects.create_user(
            email="test@gmail.com", contact=1234567890, password="1234")

        self.assertEqual(user.email, "test@gmail.com")
        self.assertTrue(user.is_active)
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
            user_model.objects.create_superuser(
                email="", contact="", password="")


class UserRegistrationTest(APITestCase):
    """This class test the user registration scenario. this is a api-level testing not view level.

    Test Cases:
        Test 1:  User registration should succeed if not existing
        Test 2:  User registration should fail if existing
        Test 3: Logged-in user should not able to register any and will have to fail. 
    """
    test_user_1 = {
        'email': 'aman.sasingh@gmail.com',
        "first_name": "Aman",
        "last_name": "singh",
        "contact": 1234567820,
        "password": "1234#Admin@Admin",
        "password1": "1234#Admin@Admin"
    }
    test_user_2 = {
        "email": "test_user@gmail.com",
        "first_name": "Test",
        "last_name": "User",
        "contact": 1234567820,
        "password": "1234",
        "password1": "1234"
    }

    def test_register_test_user_1(self):
        """Creating User account for test_user_1"""
        url = reverse('signup')
        response = self.client.post(url, data=self.test_user_1)
        self.assertEqual(response.status_code, 201)
        # deepcopy of test_user 1
        user_response = copy.deepcopy(self.test_user_1)
        user_response.pop("password")
        user_response.pop("password1")
        user_response['contact'] = str(user_response.get('contact'))
        self.assertDictEqual(
            response.json()["resultObject"], user_response)
    
    def test_register_test_user_2(self):
        """Creating User account for test_user_2"""
        url = reverse('signup')
        response = self.client.post(url, data=self.test_user_2)
        self.assertEqual(response.status_code, 201)
        # deepcopy of test_user 1
        user_response = copy.deepcopy(self.test_user_2)
        user_response.pop("password")
        user_response.pop("password1")
        user_response['contact'] = str(user_response.get('contact'))
        self.assertDictEqual(
            response.json()["resultObject"], user_response)
    
    def test_already_register_test_user_1_will_fail(self):
        """Creating User account for test_user_1"""
        url = reverse('signup')
        response = self.client.post(url, data=self.test_user_1)
        self.assertEqual(response.status_code, 201)
        response2 = self.client.post(url, data=self.test_user_1)
        self.assertEqual(response2.status_code, 400)

    def test_contact_number_should_be_unique(self):
        """Register with test_user_1 and then update email and then agin try to create a user with same contact and it should have to fail."""
        test_user_3 = copy.deepcopy(self.test_user_1)
        # first register with test_user_1
        url = reverse('signup')
        response = self.client.post(url, data=self.test_user_1)
        self.assertEqual(response.status_code, 201)

        # Update the email
        test_user_3['email'] = "testUser3@gmail.com"
        response2 = self.client.post(url, data=test_user_3)
        self.assertEqual(response2.status_code, 400)
        response_json = response2.json()
        self.assertEqual(response_json["hasError"], True)
        self.assertEquals(response_json["errors"]['contact'], ['This field must be unique.'])

        


class GetRequestedUserDetailTest(APITestCase):
    """This class use to test following scenario---

    Test Cases--
        Test 1:  Unauthenticated User Details-Request should not return any detail.
        Test 2:  Authenticated User Details-Request should show normal infos (more than unauthenticated, less than admin/staff
                                                or the same user requesting their own information)
        Test 3:  Authenticated User Details-Request should give all infos to same user.
        Test 4: Admin/Staff user can get detail of any user but not password any other detail which user do not want to share.
    """
    ...


class UserLoginTest(APITestCase):
    test_user_1 = {
        'email': 'testUser1@gmail.com',
        "first_name": "Aman",
        "last_name": "singh",
        "contact": 1234567890,
        "password": "admin@1234",
        "password1": "admin@1234"
    }
    test_user_2 = {
        "email": "testUser2@gmail.com",
        "first_name": "Test",
        "last_name": "User",
        "contact": 1234567899,
        "password": "admin@1234",
        "password1": "admin@1234"
    }

    @classmethod
    def setUpClass(cls) -> None:
        # Adding Two user with name testUser1 and testUser2 before running test in this class.
        url = reverse('signup')
        client = APIClient()
        response = client.post(url, data=cls.test_user_1)
        assert response.status_code == 201
        response = client.post(url, data=cls.test_user_2)
        assert response.status_code == 201
        return super().setUpClass()

    def test_user_login(self):
        request_data = {
            "email": "testUser1@gmail.com",
            "password": "admin@1234"
        }
        url = reverse("auth")
        response = self.client.post(url, data=request_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([key for key in response.json().keys()], [
                         "refresh", "access"])
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
