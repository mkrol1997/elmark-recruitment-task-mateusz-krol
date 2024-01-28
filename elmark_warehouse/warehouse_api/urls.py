from django.urls import path

from .views import CategoriesView, CategoryDetailView, PartDetailView, PartsView

urlpatterns = [
    path("categories/", CategoriesView.as_view()),
    path("categories/<str:name>", CategoryDetailView.as_view()),
    path("parts/", PartsView.as_view()),
    path("parts/<str:serial_number>", PartDetailView.as_view()),
]
