from django.urls import path

from .schema import schema_view
from .views import CategoriesView, CategoryDetailView, PartDetailView, PartsView

urlpatterns = [
    path("categories/", CategoriesView.as_view()),
    path("categories/<str:name>", CategoryDetailView.as_view()),
    path("parts/", PartsView.as_view()),
    path("parts/<str:serial_number>", PartDetailView.as_view()),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
