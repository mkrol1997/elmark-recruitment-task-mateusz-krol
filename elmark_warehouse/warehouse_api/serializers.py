from typing import Any, Optional, OrderedDict

from rest_framework_mongoengine import serializers

from .models import Categories, PartLocation, Parts
from .validators import CategoriesValidators, PartsValidators


class CategoriesSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Categories
        fields = ["name", "parent_name"]

    def validate_parent_name(self, parent_name: str) -> Optional[str]:
        CategoriesValidators.validate_parent_name(parent_name)
        return parent_name

    def to_representation(self, instance) -> OrderedDict[Any, Any | None]:
        queryset = super().to_representation(instance)
        queryset.pop("id", None)
        return queryset


class PartLocationSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = PartLocation
        fields = "__all__"


class PartsSerializer(serializers.DocumentSerializer):
    location = PartLocationSerializer()

    class Meta:
        model = Parts
        fields = ["serial_number", "name", "description", "category", "quantity", "price", "location"]

    def validate_category(self, category_name: str) -> Optional[str]:
        PartsValidators.validate_part_category_exists(category_name)
        PartsValidators.validate_is_part_category_subcategory(category_name)
        return category_name

    def to_representation(self, instance) -> OrderedDict[Any, Any | None]:
        queryset = super().to_representation(instance)
        queryset.pop("id", None)
        return queryset
