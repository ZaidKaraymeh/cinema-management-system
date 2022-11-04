from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('movies/add', views.add_movie, name="add_movie"),
    path('movies', views.list_movies, name="list_movies"),
] 
