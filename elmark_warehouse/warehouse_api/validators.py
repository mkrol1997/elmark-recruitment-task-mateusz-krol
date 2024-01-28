from __future__ import annotations

from typing import Optional

from rest_framework.serializers import ValidationError

from .models import Categories, Parts


class CategoriesValidators:
    @classmethod
    def validate_parent_name(cls, parent_name: Optional[str]) -> None:
        if parent_name:
            parent_category = Categories.objects(name__iexact=parent_name).first()
            cls._validate_does_parent_category_exist(parent_category)
            cls._validate_is_category_base_category(parent_category)

    @staticmethod
    def validate_is_category_base_category(category_name: str) -> None:
        base_categories = [
            category.name for category in Categories.objects(name__iexact=category_name, parent_name__exists=False)
        ]
        if category_name in base_categories:
            raise ValidationError(
                f"Can not assign base category '{category_name}' to a Part document. Choose category from subcategories"
            )

    @staticmethod
    def validate_category_has_parts_assigned(category_name: str) -> None:
        parts_assigned = Parts.objects.filter(category__iexact=category_name).first()
        if parts_assigned:
            raise ValidationError("Can not remove category with parts assigned to it")

    @staticmethod
    def validate_subcategory_has_parts_assigned(category_name: str) -> None:
        subcategories = [category.name for category in Categories.objects(parent_name__iexact=category_name)]
        parts_assigned = Parts.objects(category__in=subcategories)
        if parts_assigned:
            raise ValidationError("Can not remove category with parts assigned to it subcategory")

    @staticmethod
    def _validate_does_parent_category_exist(parent_document: Categories) -> None:
        if not parent_document:
            raise ValidationError("Invalid parent_name category. Category does not exist.")

    @staticmethod
    def _validate_is_category_base_category(parent_document: Categories) -> None:
        if parent_document.parent_name:
            raise ValidationError("Invalid parent_name category. Given parent_name category is not a base category.")


class PartsValidators:
    @staticmethod
    def validate_part_category_exists(category_name: str) -> None:
        part_category = Categories.objects(name__iexact=category_name).first()
        if not part_category:
            raise ValidationError(f"Invalid category name. {category_name} does not exist.")

    @staticmethod
    def validate_is_part_category_subcategory(category_name: str) -> None:
        part_category = Categories.objects(name__iexact=category_name).first()
        if not part_category.parent_name:
            raise ValidationError(
                f"Invalid category name. Base category {category_name} can not be assigned to a part."
            )
