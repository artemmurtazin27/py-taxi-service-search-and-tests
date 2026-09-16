from django.test import TestCase

from taxi.forms import DriverSearchForm


class DriverSearchFormTests(TestCase):
    def test_search_form_valid(self):
        form_data = {"username": "user"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])

    def test_search_form_valid_empty(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")
