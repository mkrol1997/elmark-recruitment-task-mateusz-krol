from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Warehouse API",
        default_version="v1",
        description="Warehouse API created as a recruitment task for recruitment purposes",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

categories_query_parameters = [
    openapi.Parameter(
        name="name",
        in_=openapi.IN_QUERY,
        description="Filter by category name, containing given substring (case-insensitive)",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name="parent_name",
        in_=openapi.IN_QUERY,
        description="Filter by category parent_name, containing given substring (case-insensitive)",
        type=openapi.TYPE_STRING,
    ),
]

parts_query_parameters = [
    openapi.Parameter(
        name="serial_number",
        in_=openapi.IN_QUERY,
        description="Filter by part serial_number, containing given substring (case-insensitive)",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name="name",
        in_=openapi.IN_QUERY,
        description="Filter by part name, containing given substring (case-insensitive)",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name="description",
        in_=openapi.IN_QUERY,
        description="Filter by part description, containing given substring (case-insensitive)",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name="category",
        in_=openapi.IN_QUERY,
        description="Filter by part category, containing given substring (case-insensitive)",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name="price_min",
        in_=openapi.IN_QUERY,
        description="Filter by minimum price. "
        "Returns parts collection with price greater than or equal to the given value",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="price_max",
        in_=openapi.IN_QUERY,
        description="Filter by maximum price. "
        "Returns parts collection with price lower than or equal to the given value",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="quantity_min",
        in_=openapi.IN_QUERY,
        description="Filter by minimum quantity. "
        "Returns parts collection with quantity greater than or equal to the given value",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="quantity_max",
        in_=openapi.IN_QUERY,
        description="Filter by maximum quantity. "
        "Returns parts collection with quantity lower than or equal to the given value",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="room",
        in_=openapi.IN_QUERY,
        description="Filter by location room name, containing given substring (case-insensitive)",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name="bookcase",
        in_=openapi.IN_QUERY,
        description="Filter by location bookcase number",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="shelf",
        in_=openapi.IN_QUERY,
        description="Filter by location shelf number",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="cuvette",
        in_=openapi.IN_QUERY,
        description="Filter by location cuvette number",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="column",
        in_=openapi.IN_QUERY,
        description="Filter by location column number",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="row",
        in_=openapi.IN_QUERY,
        description="Filter by location row number",
        type=openapi.TYPE_NUMBER,
    ),
]
