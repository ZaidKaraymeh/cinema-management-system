from django.urls import path

from core.views import customer_views

urlpatterns = [
    path('book/<str:schedule_id>', customer_views.customer_movie_booking, name="customer_movie_booking"),
    path('ticket/<str:schedule_id>/<str:user_id>', customer_views.book_ticket_json, name="book_ticket_json"),
]
