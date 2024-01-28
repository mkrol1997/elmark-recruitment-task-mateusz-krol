from drf_yasg.utils import swagger_auto_schema
from rest_framework_mongoengine.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .filters import CategoriesFilter, PartsFilter
from .models import Categories, Parts
from .schema import categories_query_parameters, parts_query_parameters
from .serializers import CategoriesSerializer, PartsSerializer
from .validators import CategoriesValidators


class CategoriesView(ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a collection of categories filtered using available parameters.",
        manual_parameters=categories_query_parameters,
        omit_fields=("id",),
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        return CategoriesFilter(self.request.query_params, queryset=queryset).qs


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = "name"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.parent_name:
            CategoriesValidators.validate_category_has_parts_assigned(category_name=instance.name)
            return self.destroy(request, *args, **kwargs)
        else:
            CategoriesValidators.validate_subcategory_has_parts_assigned(category_name=instance.name)
        return self.destroy(request, *args, **kwargs)


class PartsView(ListCreateAPIView):
    queryset = Parts.objects.all()
    serializer_class = PartsSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a collection of categories filtered using available parameters.",
        manual_parameters=parts_query_parameters,
        omit_fields=("id",),
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        return PartsFilter(self.request.query_params, queryset=self.queryset).qs


class PartDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Parts.objects.all()
    serializer_class = PartsSerializer
    lookup_field = "serial_number"
