from django.test import TestCase
from apps.resources.form import PostResourceForm


# Test Case # Test<form-name>Form
class TestPostResourceForm(TestCase):
    # unit test 1
    def test_form_is_valid_method_return_true_for_good_data(self):
        # ARRANGE
        data = {
            "title": "Python for beginners",
            "link": "https://pythonforbeginners.com",
            "description": "Best resource for beginners and free",
            # TODO: Add more key-value pairs base on your form
        }
        # Act
        form = PostResourceForm(data=data)

        # Assert
        self.assertTrue(form.is_valid())

    def test_form_missing_link_generate_errors(self):
        data = {
            "title": "Python for beginners",
            # "link": "https://pythonforbeginners.com",
            "description": "Best resource for beginners and free",
            # TODO: Add more key-value pairs base on your form
        }
        # Act
        form = PostResourceForm(data=data)
        form.is_valid()  # This is needed for the form to generate any errors.

        # Assert
        # self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["link"], ["This field is required."])