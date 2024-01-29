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

    price_min = filters.NumberFilter(name="price", label="price_min", lookup_type="gte")
    price_max = filters.NumberFilter(name="price", label="price_max", lookup_type="lte")
    quantity_min = filters.NumberFilter(name="quantity", label="quantity_min", lookup_type="gte")
    quantity_max = filters.NumberFilter(name="quantity", label="quantity_max", lookup_type="lte")
    room = filters.StringFilter(name="location__room", label="room", lookup_type="icontains")
    bookcase = filters.NumberFilter(name="location__bookcase", label="bookcase")
    shelf = filters.NumberFilter(name="location__shelf", label="shelf")
    cuvette = filters.NumberFilter(name="location__cuvette", label="cuvette")
    column = filters.NumberFilter(name="location__column", label="column")
    row = filters.NumberFilter(name="location__row", label="row")

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
