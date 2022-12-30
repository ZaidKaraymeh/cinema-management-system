from django.urls import path

from core.views import customer_views

urlpatterns = [
    path('movie_booking/<str:schedule_id>', customer_views.customer_movie_booking, name="customer_movie_booking"),
]
