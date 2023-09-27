from django.test import TestCase
from apps.resources import models


# Test Case class # Test<model-name>Model
class TestTagModel(TestCase):
    def setUp(self) -> None:
        self.tag_name = "Python"
        self.tag = models.Tag(name=self.tag_name)

    # unit test 1 # test_<logic-name>
    def test_create_tag_object_successful(self):
        # Check if the object created is of the instance Tag
        self.assertIsInstance(self.tag, models.Tag)

    # unit test 2
    def test_dunder_str(self):
        # str(self.tag) or self.tag.__str__()
        self.assertEqual(str(self.tag), self.tag_name)

    # TODO: Test all models