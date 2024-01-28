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
        description="Filter by name, containing given substring (case-insensitive)",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name="parent_name",
        in_=openapi.IN_QUERY,
        description="Filter by parent_name, containing given substring (case-insensitive)",
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
        name="price_0",
        in_=openapi.IN_QUERY,
        description="Minimum price range. Returns parts collection with prices greater than or equal to the given value. NOTICE: Use only with price_1 in order to declare maximum price range",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="price_1",
        in_=openapi.IN_QUERY,
        description="Maximum price range. Returns parts collection with prices lower than or equal to the given value NOTICE: Use only with price_0 in order to declare minimum price range",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="quantity_0",
        in_=openapi.IN_QUERY,
        description="Filter by minimum quantity. Returns parts collection with quantity greater than or equal to the given value",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="quantity_1",
        in_=openapi.IN_QUERY,
        description="Filter by maximum quantity. Return parts collection with prices lower than or equal to the given value",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="location__room",
        in_=openapi.IN_QUERY,
        description="Filter by room name location, containing given substring (case-insensitive)",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name="location__bookcase",
        in_=openapi.IN_QUERY,
        description="Filter by bookcase number location",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="location__shelf",
        in_=openapi.IN_QUERY,
        description="Filter by shelf number location ",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="location__cuvette",
        in_=openapi.IN_QUERY,
        description="Filter by cuvette number location",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="location__column",
        in_=openapi.IN_QUERY,
        description="Filter by column number location",
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name="location__row",
        in_=openapi.IN_QUERY,
        description="Filter by row number location",
        type=openapi.TYPE_NUMBER,
    ),
]
