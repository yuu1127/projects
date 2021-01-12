from django.urls import path
from . import views

app_name = "movie"

urlpatterns = [
    path('<int:movie_id>', views.display_detail, name="movie_detail"),
    path('<int:movie_id>/add_review', views.add_review, name='add_review'),
    path('<int:movie_id>/edit_review', views.edit_review, name='edit_review'),
]
