from __future__ import annotations

import sys
from unittest import TestCase

import mongoengine
import mongomock
from pymongo import MongoClient
from rest_framework.serializers import ValidationError
from rest_framework.test import APIClient

from .models import Categories, Parts


def switch_db_connection() -> MongoClient:
    mongoengine.connection.disconnect()
    client = mongoengine.connect(
        "mongoengine_uts_db", host="mongodb://localhost", mongo_client_class=mongomock.MongoClient, alias="default"
    )
    return client


if "test" in sys.argv:
    db_client = switch_db_connection()


class TestCategoriesViews(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()

    def tearDown(self) -> None:
        db_client.drop_database("mongoengine_uts_db")

    def test_should_return_status_200_for_categories_get_method(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)

    def test_should_return_empty_queryset_for_non_existing_filter_value(self):
        response = self.client.get("/api/categories/?name=power")
        expected, result = 0, len(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, result)

    def test_should_return_304_for_valid_categories_post_method(self):
        data = {"name": "test_name", "parent_name": ""}

        response = self.client.post("/api/categories/", data)

        self.assertEqual(response.status_code, 201)
        result = Categories.objects(name="test_name").first()

        self.assertEqual(result.name, "test_name")

    def test_should_raise_validation_error_when_not_specified_all_required_category_data_for_post_method(self):
        data = {"name": "test_name"}
        response = self.client.post("/api/categories/", data)

        self.assertEqual(response.status_code, 400)
        self.assertRaises(ValidationError)

    def test_should_raise_validation_error_when_patching_parent_name_with_self_name(self):
        data = {"name": "test_name", "parent_name": "distinct_name"}
        response = self.client.post("/api/categories/", data)

        self.client.patch("/api/categories/test_name", data={"parent_name": "test_name"})
        self.assertEqual(response.status_code, 400)
        self.assertRaises(ValidationError)

    def test_should_raise_validation_error_when_patching_parent_name_with_self_name_using_put_method(self):
        data = {"name": "test_name", "parent_name": "distinct_name"}
        response = self.client.post("/api/categories/", data)

        self.client.put("/api/categories/test_name", data={"name": "test_name", "parent_name": "test_name"})
        self.assertEqual(response.status_code, 400)
        self.assertRaises(ValidationError)

    def test_should_return_true_when_category_removed(self):
        name, parent_name = "uts_name", ""

        Categories(name=name, parent_name=parent_name).save()

        response = self.client.delete(f"/api/categories/{name}")
        result, expected = Categories.objects(name=name).count(), 0

        self.assertEqual(response.status_code, 204)
        self.assertEqual(result, expected)

    def test_should_raise_validation_error_when_assigning_subcategory_to_non_existing_base_category(self):
        data = {"name": "subcategory", "parent_name": "base_category"}

        response = self.client.post("/api/categories/", data=data)

        self.assertEqual(response.status_code, 400)
        self.assertRaises(ValidationError)

    def test_should_raise_validation_error_for_unique_name_rule_violation(self):
        Categories(name="base", parent_name="").save()

        data = {"name": "base", "parent_name": "parent_name"}

        response = self.client.post("/api/categories/", data=data)

        expected, result = 1, Categories.objects.all().count()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected, result)


class TestPartsViews(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def tearDown(self) -> None:
        db_client.drop_database("mongoengine_uts_db")

    def create_category_tree(self) -> None:
        Categories(name="base", parent_name="").save()
        Categories(name="test_subcategory", parent_name="base").save()

    def create_test_part(self) -> None:
        part_location = {"room": "Test room", "bookcase": 1, "shelf": 2, "cuvette": 3, "column": 3, "row": 2}
        Parts(
            serial_number="test_serial",
            name="test_name",
            description="test description",
            category="test_subcategory",
            price=100,
            quantity=10,
            location=part_location,
        ).save()

    def test_should_raise_validation_error_when_creating_part_with_non_existing_category(self):
        data = {
            "serial_number": "test_serial",
            "name": "test_name",
            "description": "test description",
            "category": "test_subcategory",
            "price": 100,
            "quantity": 10,
            "location": {"room": "Test room", "bookcase": 1, "shelf": 2, "cuvette": 3, "column": 3, "row": 2},
        }

        response = self.client.post("/api/parts/", data=data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertRaises(ValidationError)

    def test_should_return_true_when_part_successfully_created(self):
        data = {
            "serial_number": "test_serial",
            "name": "test_name",
            "description": "test description",
            "category": "test_subcategory",
            "price": 100,
            "quantity": 10,
            "location": {"room": "Test room", "bookcase": 1, "shelf": 2, "cuvette": 3, "column": 3, "row": 2},
        }

        self.create_category_tree()
        response = self.client.post("/api/parts/", data=data, format="json")

        expected, result = 1, Parts.objects(category="test_subcategory").count()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(expected, result)

    def test_should_raise_validation_error_when_not_specified_all_required_part_data_for_post_method(self):
        data = {
            "serial_number": "test_serial",
            "name": "test_name",
            "quantity": 10,
            "location": {"room": "Test room", "cuvette": 3, "row": 2},
        }
        response = self.client.post("/api/parts/", data=data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertRaises(ValidationError)

    def test_should_return_true_when_part_successfully_updated_with_patch_method(self):
        self.create_category_tree()
        self.create_test_part()

        data = {
            "name": "updated_name",
            "quantity": 13,
        }

        part_document = Parts.objects(name="test_name").first()

        response = self.client.patch(f"/api/parts/{part_document.serial_number}", data=data)

        updated_part = Parts.objects(name="updated_name").first()
        expected_name, result_name = "updated_name", updated_part.name
        expected_quantity, result_quantity = 13, updated_part.quantity

        self.assertEqual(expected_name, result_name)
        self.assertEqual(expected_quantity, result_quantity)

        self.assertEqual(response.status_code, 200)

    def test_should_return_status_code_200_for_detailed_part_view(self):
        self.create_category_tree()
        self.create_test_part()

        response = self.client.get("/api/parts/test_serial")
        expected, result = "test_serial", response.data.get("serial_number")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, result)

    def test_should_return_true_for_successful_part_deletion(self):
        self.create_category_tree()
        self.create_test_part()

        response = self.client.delete("/api/parts/test_serial")
        expected, result = 1, Parts.objects(serial_number="test_serial").count()

        self.assertEqual(response.status_code, 204)
        self.assertNotEqual(expected, result)

    def test_should_raise_validation_error_for_unique_serial_number_rule_violation(self):
        data = {
            "serial_number": "test_serial",
            "name": "unique_name",
            "description": "unique description",
            "category": "test_subcategory",
            "price": 1000,
            "quantity": 100,
            "location": {"room": "unique room", "bookcase": 2, "shelf": 4, "cuvette": 5, "column": 6, "row": 2},
        }

        self.create_category_tree()
        self.create_test_part()

        response = self.client.post("/api/parts/", data=data, format="json")
        expected, result = 1, Parts.objects.all().count()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected, result)
