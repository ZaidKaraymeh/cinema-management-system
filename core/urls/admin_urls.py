from django.urls import path

from core.views import admin_views
from payments import views as payment_views
urlpatterns = [
    path('dashboard', admin_views.dashboard, name="dashboard"),
    path('staff/movies/add', admin_views.add_movie, name="add_movie"),
    path('staff/movies/edit/<str:movie_id>',
         admin_views.edit_movie, name="edit_movie"),
    path('staff/movies/delete/<str:movie_id>',
         admin_views.delete_movie, name="delete_movie"),
     path('staff/hall/delete/<str:hall_id>', admin_views.delete_hall, name="delete_hall"),

    path('staff/topups', admin_views.list_topups, name="list_topups"),
    path('staff/transactions', admin_views.list_transactions, name="list_transactions"),
    path('staff/tickets/<str:transaction_id>', admin_views.list_tickets, name="list_tickets"),
    path('staff/transaction/approve/<str:transaction_id>', admin_views.approve_transaction, name="approve_transaction"),

    path('staff/movies', admin_views.list_movies, name="list_movies"),
    path('staff/schedules/add', admin_views.schedule_movie, name="schedule_movie"),
    path('staff/schedules/edit/<str:schedule_id>',
         admin_views.edit_schedule_movie, name="edit_schedule_movie"),
    path('staff/schedules/', admin_views.list_schedule_movies,
         name="list_schedule_movies"),
    path('staff/schedules/delete/<str:schedule_id>', admin_views.delete_movie_schedule,
         name="delete_movie_schedule"),
    path('staff/slots/<str:hall_id>/<str:date>',
         admin_views.slots_available_json, name="slots_available_json"),
    path('staff/customers',
         admin_views.list_customers, name="list_customers"),
    path('staff/employees',
         admin_views.list_employees, name="list_employees"),
    

    path('staff/halls', admin_views.list_halls, name="list_halls"),
    path('staff/halls/add', admin_views.add_hall, name='add_hall'),
    path('staff/customers/delete/<str:customer_id>', admin_views.delete_customer, name="delete_customer"),
     path('staff/employees/delete/<str:employee_id>', admin_views.delete_employee, name="delete_employee"),
     path('staff/export', admin_views.export, name="export"),
]
