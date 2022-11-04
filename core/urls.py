from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('movies/add', views.add_movie, name="add_movie"),
    path('movies/edit/<str:movie_id>', views.edit_movie, name="edit_movie"),
    path('movies/delete/<str:movie_id>', views.delete_movie, name="delete_movie"),
    path('movies', views.list_movies, name="list_movies"),
] 

"""asdasdasdasd 
asd
asd
asd
 asd
 assert"""