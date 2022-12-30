from django.urls import path

from core.views import customer_views

urlpatterns = [
    path('customer/movie_booking', customer_views.customer_movie_booking, name="customer_movie_booking"),
]
