from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="name-test",
            country="test-country",
        )
        Manufacturer.objects.create(
            name="name2-test",
            country="test2-country",
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test-username",
            password="test1234",
        )
        self.client.force_login(self.user)

        self.driver1 = get_user_model().objects.create_user(
            username="test-driver1",
            license_number="ABC11111",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="test-driver2",
            license_number="ABC22222",
        )
        self.driver3 = get_user_model().objects.create_user(
            username="driver3",
            license_number="ABC33333",
        )

    def test_search_drivers(self):
        response = self.client.get(
            DRIVER_URL, {"username": "test"}
        )
        self.assertEqual(response.status_code, 200)
        drivers_context = response.context["driver_list"]

        self.assertIn(self.driver1, drivers_context)
        self.assertIn(self.driver2, drivers_context)
        self.assertNotIn(self.driver3, drivers_context)

    def test_create_driver(self):
        form_data = {
            "username": "user-user",
            "password1": "test-password",
            "password2": "test-password",
            "first_name": "first name",
            "last_name": "last name",
            "license_number": "ABC12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
