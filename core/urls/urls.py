from django.urls import path

from core.views import views

urlpatterns = [
    path('', views.home, name="home"),
    path('movie/<str:movie_id>', views.movie_details, name='movie_details')
    
] 
