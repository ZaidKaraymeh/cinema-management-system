from django.urls import path

from core.views import customer_views

urlpatterns = [
    path('book/<str:schedule_id>', customer_views.customer_movie_booking, name="customer_movie_booking"),
    path('payment/<str:schedule_id>/<str:user_id>', customer_views.book_ticket_json, name="book_ticket_json"),
    #path('tickets/<str:transaction_id>', customer_views.tickets, name="tickets"),
    path('tickets/<str:transaction_id>', customer_views.tickets, name="tickets"),
    path('transactions', customer_views.transaction_history, name="transactions"),
    path('topups', customer_views.topup_history, name="topups"),
]
