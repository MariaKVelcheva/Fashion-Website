from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from fashionWebsite.accounts.models import Customer

AppUser = get_user_model()


class CustomerModelTest(TestCase):

    def setUp(self):
        self.user = AppUser.objects.create_user(
            email="test@test.com",
            password="testingtest123",
        )
        self.customer = Customer.objects.get_or_create(user=self.user)[0]

    def test_is_profile_complete_all_fields(self):
        self.customer.first_name = "Ivan"
        self.customer.last_name = "Ivanov"
        self.customer.address = "123 Sofia"
        self.customer.telephone_number = "123456789"
        self.customer.save()
        self.assertTrue(self.customer.is_profile_complete())

    def test_is_profile_complete_missing_first_name(self):
        self.customer.first_name = ""
        self.customer.last_name = "Ivanov"
        self.customer.address = "123 Sofia"
        self.customer.telephone_number = "123456789"
        self.customer.save()
        self.assertFalse(self.customer.is_profile_complete())

    def test_is_profile_complete_short_name(self):
        self.customer.first_name = "Iv"
        self.customer.last_name = "Ivanov"
        self.customer.address = "123 Sofia"
        self.customer.telephone_number = "123456789"
        self.customer.save()
        self.assertFalse(self.customer.is_profile_complete())

    def test_is_profile_complete_missing_address(self):
        self.customer.first_name = "Ivan"
        self.customer.last_name = "Ivanov"
        self.customer.address = ""
        self.customer.telephone_number = "123456789"
        self.customer.save()
        self.assertFalse(self.customer.is_profile_complete())

    def test_full_name_property(self):
        self.customer.first_name = "Ivan"
        self.customer.last_name = "Ivanov"
        self.customer.save()
        self.assertEqual(self.customer.full_name, "Ivan Ivanov")

    def test_loyalty_points_default_zero(self):
        self.assertEqual(self.user.loyalty_points, 0)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = AppUser.objects.create_user(
            email="test@test.com",
            password="testingtest123",
        )

    def test_login_valid_credentials(self):
        response = self.client.post(reverse("login"), {
            "username": "test@test.com",
            "password": "testingtest123",
        })
        self.assertRedirects(response, reverse("home"))

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse("login"), {
            "username": "test@test.com",
            "password": "testedpassword",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_merges_session_cart(self):
        session = self.client.session
        session["cart"] = {"1": 2}
        session.save()

        self.client.post(reverse("login"), {
            "username": "test@test.com",
            "password": "testingtest123",
        })

        self.assertNotIn("cart", self.client.session)
