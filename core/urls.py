from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('movie', views.add_movie, name="add_movie")
] 
