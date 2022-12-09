from django.urls import path

from .views import views
from .views import admin_views
from .views import customer_views


urlpatterns = [
    path('', views.home, name="home"),
    path('movies/add', views.add_movie, name="add_movie"),
    path('movies/edit/<str:movie_id>', views.edit_movie, name="edit_movie"),
    path('movies/delete/<str:movie_id>', views.delete_movie, name="delete_movie"),
    path('movies', views.list_movies, name="list_movies"),
    path('schedules/add', views.schedule_movie, name="schedule_movie"),
    path('schedules/', views.list_schedule_movies, name="list_schedule_movies"),
    path('slots/<str:hall_id>/<str:date>', views.slots_available_json, name="slots_available_json"),
] 
