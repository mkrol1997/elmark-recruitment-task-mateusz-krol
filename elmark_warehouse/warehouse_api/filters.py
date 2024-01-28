from django.conf import settings
from django_mongoengine_filter import FilterSet, filters

from .models import Categories, Parts


class CategoriesFilter(FilterSet):
    filter_overrides = settings.FILTER_CONFIG

    class Meta:
        model = Categories
        fields = ["name", "parent_name"]


class PartsFilter(FilterSet):
    filter_overrides = settings.FILTER_CONFIG
    price = filters.RangeFilter()
    quantity = filters.RangeFilter()

    class Meta:
        model = Parts
        fields = [
            "serial_number",
            "name",
            "description",
            "category",
            "quantity",
            "price",
            "location__room",
            "location__bookcase",
            "location__shelf",
            "location__cuvette",
            "location__column",
            "location__row",
        ]
