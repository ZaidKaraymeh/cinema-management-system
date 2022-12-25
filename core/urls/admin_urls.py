from django.urls import path

from core.views import admin_views

urlpatterns = [
    path('dashboard', admin_views.dashboard, name="dashboard"),
    path('staff/movies/add', admin_views.add_movie, name="add_movie"),
    path('staff/movies/edit/<str:movie_id>',
         admin_views.edit_movie, name="edit_movie"),
    path('staff/movies/delete/<str:movie_id>',
         admin_views.delete_movie, name="delete_movie"),
    path('staff/movies', admin_views.list_movies, name="list_movies"),
    path('staff/schedules/add', admin_views.schedule_movie, name="schedule_movie"),
    path('staff/schedules/', admin_views.list_schedule_movies,
         name="list_schedule_movies"),
    path('staff/slots/<str:hall_id>/<str:date>',
         admin_views.slots_available_json, name="slots_available_json"),
]
