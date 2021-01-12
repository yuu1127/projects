from django.urls import path, re_path
from . import views

app_name = "search"

urlpatterns = [
    path("", views.search_results, name="search_results")
]
