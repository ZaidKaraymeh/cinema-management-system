import csv
from payments.models import Topup
from django.shortcuts import render, redirect
from users.models import CustomUser
from ..models import Movie
from django.contrib import messages
from django.core.paginator import Paginator
from ..forms import *
from ..utils.helpers import *
from ..models import *
import json
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

from rest_framework.decorators import api_view
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.apps import apps
from core.decorators import is_admin
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from django.utils import timezone

@is_admin
def dashboard(request):

    return render(request, 'admin/dashboard.html')

@is_admin
def change_ticket_to_used(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.is_used = True
    ticket.save()
    return HttpResponse(f'<h1 style="color:green;" >Success - Ticket {ticket.id} Was Scanned </h1>')

@is_admin
def list_movies(request):
    if request.GET.get('search'):
        try:
            movies = Movie.objects.filter(
                title__icontains=request.GET.get('search'))
            paginator = Paginator(movies, 6)
            page_number = request.GET.get('page') or 1
            movies = paginator.get_page(page_number)
            return render(request, 'admin/movies.html', {"movies": movies})
        except Exception:
            messages.error(
                request, f"Employee with email {request.GET.get('search')} does not exist!")
            return redirect('list_movies')

    list_movies = Movie.objects.all().order_by('created_at')

    paginator = Paginator(list_movies, 10)
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)

    context = {
        "movies": movies,
    }

    return render(request, 'admin/movies.html', context)


@is_admin
def add_movie(request):
    # Make sure that the user is admin
    if request.user.is_authenticated and request.user.user_type == "ADM":
        if request.method == "POST":
            movie_form = MovieForm(request.POST, request.FILES)
            if movie_form.is_valid():
                movie = movie_form.save(commit=False)
                movie.price = Decimal('3.0')
                movie.save()
                messages.success(
                    request, f"{movie.title} has been added successfuly!")
                return redirect('list_movies')
        else:
            movie_form = MovieForm()

        context = {
            "form": movie_form,
        }
        return render(request, "admin/add_movie.html", context)
    return HttpResponse("Access Denied.")


@is_admin
def edit_movie(request, movie_id):
    user = request.user
    movie = Movie.objects.get(id=movie_id)

    if request.method == "POST":
        movie_form = MovieForm(request.POST, instance=movie)
        status_form = MovieStatusForm(request.POST)
        if movie_form.is_valid() and status_form.is_valid():
            movie = movie_form.save(commit=False)
            movie.status = status_form.cleaned_data['status']
            movie.save()
            messages.info(
                request, f"{movie.title} has been Edited successfuly!")
            return redirect('list_movies')
    else:
        movie_form = MovieForm(instance=movie)
        status_form = MovieStatusForm()

    context = {
        "form": movie_form,
        "movie": movie,
        "status_form": status_form,
    }
    return render(request, "admin/edit_movie.html", context)


@is_admin
def delete_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.delete()
    messages.error(request, f"{movie.title} has been Deleted successfuly!")

    return redirect('list_movies')


@is_admin
def list_schedule_movies(request):
    if request.GET.get('search'):
        try:
            movie_schedules = MovieSchedule.objects.filter(
                movie__title__icontains=request.GET.get('search'))
            paginator = Paginator(movie_schedules, 6)
            page_number = request.GET.get('page') or 1
            movie_schedules = paginator.get_page(page_number)
            return render(request, 'admin/list_movies_scheduled.html', {"movie_schedules": movie_schedules})
        except Exception:
            messages.error(
                request, f"Employee with email {request.GET.get('search')} does not exist!")
            return redirect('list_schedule_movies')
    movie_schedules = MovieSchedule.objects.all()

    paginator = Paginator(movie_schedules, 10)
    page_number = request.GET.get('page')
    movie_schedules = paginator.get_page(page_number)

    context = {
        'movie_schedules': movie_schedules
    }

    return render(request, 'admin/list_movies_scheduled.html', context)


@is_admin
def schedule_movie(request):
    movies = Movie.objects.filter(status="Running")
    if request.method == "POST":
        schedule_form = MovieScheduleForm(movies, request.POST)
        slot_form = SlotForm(request.POST)

        if schedule_form.is_valid():
            movie_schedule = schedule_form.save(commit=False)
            movie_schedule.slot = Slot.objects.get(
                id=slot_form['slots'].value()
            )
            hall = movie_schedule.hall.slots.add(movie_schedule.slot)
            movie_schedule.save()
            messages.success(
                request, f"{movie_schedule.movie.title} has been scheduled successfuly!")
            return redirect('list_schedule_movies')
    else:
        schedule_form = MovieScheduleForm(movies)
        slot_form = SlotForm()

    context = {
        'schedule_form': schedule_form,
        'slot_form': slot_form,
    }

    return render(request, 'admin/schedule_movie.html', context)


@is_admin
def edit_schedule_movie(request, schedule_id):
    schedule = MovieSchedule.objects.get(id=schedule_id)

    if request.method == "POST":
        schedule_form = MovieScheduleForm(request.POST, instance=schedule)
        slot_form = SlotForm(request.POST)

        if schedule_form.is_valid():
            movie_schedule = schedule_form.save(commit=False)
            movie_schedule.slot = Slot.objects.get(
                id=slot_form['slots'].value()
            )
            hall = movie_schedule.hall.slots.add(movie_schedule.slot)
            movie_schedule.save()
            messages.info(
                request, f"{movie_schedule.movie.title} has been Edited successfuly!")
            return redirect('list_schedule_movies')
    else:
        schedule_form = MovieScheduleForm(instance=schedule)
        slot_form = SlotForm()

    context = {
        'schedule_form': schedule_form,
        'slot_form': slot_form,
    }

    return render(request, 'admin/edit_schedule_movie.html', context)


@is_admin
def delete_movie_schedule(request, schedule_id):
    schedule = MovieSchedule.objects.get(id=schedule_id)
    schedule.delete()
    messages.error(request, f"{schedule.movie.title} has been Deleted successfuly!")

    return redirect('list_schedule_movies')


@is_admin
def delete_hall(request, hall_id):
    hall = Hall.objects.get(id=hall_id)
    hall.delete()
    messages.error(request, f"{hall.name} has been Deleted successfuly!")

    return redirect('list_halls')


@is_admin
def slots_available_json(request, hall_id, date):
    hall = Hall.objects.get(id=hall_id)

    slot_choices = get_time_slots(hall, date)

    response = json.dumps(dict(slot_choices))

    return HttpResponse(response)


@is_admin
def list_customers(request):
    if request.GET.get('search'):
        try:
            customers = CustomUser.objects.filter(
                email__icontains=request.GET.get('search'))
            paginator = Paginator(customers, 6)
            page_number = request.GET.get('page') or 1
            customers = paginator.get_page(page_number)
            return render(request, 'admin/list_customers.html', {"customers": customers})
        except Exception:
            messages.error(
                request, f"Customer with email {request.GET.get('search')} does not exist!")
            return redirect('list_customers')
    customers = CustomUser.objects.filter(user_type='CTM')
    paginator = Paginator(customers, 7)
    page_number = request.GET.get('page')
    customers = paginator.get_page(page_number)

    context = {
        'customers': customers,
    }
    return render(request, 'admin/list_customers.html', context)


@is_admin
def list_employees(request):
    if request.GET.get('search'):
        try:
            employees = CustomUser.objects.filter(
                email__icontains=request.GET.get('search'), user_type='ADM')
            paginator = Paginator(employees, 6)
            page_number = request.GET.get('page') or 1
            employees = paginator.get_page(page_number)
            return render(request, 'admin/list_employees.html', {"employees": employees})
        except Exception:
            messages.error(
                request, f"Employee with email {request.GET.get('search')} does not exist!")
            return redirect('list_employees')

    employees = CustomUser.objects.filter(user_type='ADM')
    paginator = Paginator(employees, 7)
    page_number = request.GET.get('page')
    employees = paginator.get_page(page_number)

    context = {
        'employees': employees,
    }
    return render(request, 'admin/list_employees.html', context)

# Todo 
def view_customer_ticket_history(request):
    pass


@is_admin
def list_halls(request):
    if request.GET.get('search'):
        try:
            halls = Hall.objects.filter(
                name__icontains=request.GET.get('search'))
            paginator = Paginator(halls, 6)
            page_number = request.GET.get('page') or 1
            halls = paginator.get_page(page_number)
            return render(request, 'admin/list_halls.html', {"halls": halls})
        except Exception:
            messages.error(
                request, f"Employee with email {request.GET.get('search')} does not exist!")
            return redirect('list_halls')
    halls = Hall.objects.all()
    paginator = Paginator(halls, 6)
    page_number = request.GET.get('page')
    halls = paginator.get_page(page_number)

    context = {
        'halls': halls,
    }

    return render(request, 'admin/list_halls.html', context)


@is_admin
def add_hall(request):

    classes = ['A', 'B', 'C', 'D', 'E', 'F']

    if request.method == 'POST':
        hall_form = HallForm(request.POST)
        if hall_form.is_valid():
            hall = hall_form.save(commit=False)
            hall.save()
            for obj in classes:
                for count in range(1, 9):
                    seat = Seat.objects.create(
                        name=f"{obj}{count}",
                        type = "VIP" if obj == "A" or obj == "B" else "NRM"
                    )
                    seat.save()
                    hall.seats.add(seat)
            messages.success(
                request, f"{hall.name} has been added successfuly!")
            return redirect('list_halls')
    else:
        hall_form = HallForm()
    
    context = {
        'form': hall_form,
    }

    return render(request, 'admin/add_hall.html', context)


@is_admin
def delete_customer(request, customer_id):
    customer = CustomUser.objects.get(id=customer_id)
    customer.delete()
    messages.error(request, f"{customer.email} has been Deleted successfuly!")

    return redirect('list_customers')


@is_admin
def delete_employee(request, employee_id):
    employee = CustomUser.objects.get(id=employee_id)
    employee.delete()
    messages.error(request, f"{employee.email} has been Deleted successfuly!")

    return redirect('list_employees')


@is_admin
def list_topups(request):
    if request.GET.get('search'):
        try:
            topups = Topup.objects.filter(
                user__email__icontains=request.GET.get('search')).order_by('is_approved')
            paginator = Paginator(topups, 6)
            page_number = request.GET.get('page') or 1
            topups = paginator.get_page(page_number)
            return render(request, 'admin/list_topups.html', {"topups": topups})
        except Exception:
            messages.error(
                request, f"Topup with email {request.GET.get('search')} does not exist!")
            return redirect('list_topups')
    
    topups = Topup.objects.all().order_by('is_approved')

    context = {
        "topups": topups
    }

    return render(request, 'admin/list_topups.html', context)


@is_admin
def export(request):
    core_models = apps.get_app_config('core').get_models()
    payments_models = apps.get_app_config('payments').get_models()
    users_models = apps.get_app_config('users').get_models()
    choices = []
    for model in core_models:
        choices.append((model.__name__, model.__name__))

    for model in payments_models:
        choices.append((model.__name__, model.__name__))

    for model in users_models:
        choices.append((model.__name__, model.__name__))
    if request.method == 'POST':
        form = ExportForm(choices, request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            model_name = form.cleaned_data['choices']
            
            app_labels = ['payments', 'core', 'users']
            for app in app_labels:
                try:
                    model_obj = apps.get_model(app, model_name).objects.filter(
                        created_at__range=[
                        start_date, end_date]
                        )
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = f'attachment; filename="{model_name}s-{datetime.now()}.csv"'

                    writer = csv.writer(response)
                    headers = [field.name for field in model_obj.model._meta.fields]
                    headers.append(f"Date of Report: {timezone.now()}")
                    headers.append(f"From Date: {start_date}")
                    headers.append(f"To Date: {start_date}")
                    writer.writerow(headers)

                    for instance in model_obj:
                        # write all the instances
                        writer.writerow([str(getattr(instance, field.name)) for field in instance._meta.fields])
                    return response
                except Exception as e:
                    print(e)
                    continue
    else:
        

        form = ExportForm(choices=choices)
    
    context = {
        'form': form,
    }

    return render(request, 'admin/export.html', context)


# from django.apps import apps

#     def model_fields(model_name):

#         model_obj = apps.get_model("core", model_name).objects.filter()
#         field_names = [field.name for field in model_obj.model._meta.get_fields()]
#         print(field_names)
#         for instance in model_obj:
#             # field_values_str = [str(getattr(instance, field.name)) for field in instance._meta.get_fields()]
#             field_values_class_type = [getattr(instance, field.name)  for field in instance._meta._get_fields(reverse=False, include_parents=False)]
#             field_values = [getattr(instance, field.name) for field in instance._meta.get_fields()]
#             # print(field_values_class_name)
#             for index, field in enumerate(field_values_class_type):
#                 # print(f"{index} {field} == ManyRelatedManager", field == 'ManyRelatedManager' )
#                 if field.__class__.__name__ == 'ManyRelatedManager':
#                     print(index)


#             continue
#     model_fields("Ticket")


# list transactions
@is_admin
def list_transactions(request):
    if request.GET.get('search'):
        try:
            transactions = Transaction.objects.filter(user__email__icontains=request.GET.get('search'))
            paginator = Paginator(transactions, 6)
            page_number = request.GET.get('page') or 1
            transactions = paginator.get_page(page_number)
            return render(request, 'admin/list_transactions.html', {"transactions": transactions})
        except Exception: 
            messages.error(request, f"Transaction with id {request.GET.get('search')} does not exist!")
            return redirect('list_transactions')

    transactions = Transaction.objects.all().order_by('-created_at')
    #pagination
    paginator = Paginator(transactions, 6)
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)


    context = {
        "transactions": transactions
    }

    return render(request, 'admin/list_transactions.html', context)

# approve transaction
@is_admin
def approve_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    if transaction.isPaid:
        messages.error(request, f"{transaction.id} has already been approved!")
        return redirect('list_transactions')
    transaction.isPaid = True
    transaction.save()
    balance, created = Balance.objects.get_or_create(user=transaction.user)
    balance.balance -= transaction.amount
    balance.save()
    messages.success(request, f"{transaction} has been approved successfuly!")

    return redirect('list_transactions')

# view transaction
@is_admin
def view_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    context = {
        "transaction": transaction
    }

    return render(request, 'admin/view_transaction.html', context)

# list tickets
@is_admin
def list_tickets(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    tickets = Ticket.objects.filter(transaction=transaction_id)
    #pagination
    paginator = Paginator(tickets, 7)
    page_number = request.GET.get('page')
    tickets = paginator.get_page(page_number)
    


    context = {
        "tickets": tickets,
        "transaction": transaction
    }

    return render(request, 'admin/list_tickets.html', context)


# delete hall
@is_admin
def delete_hall(request, hall_id):
    hall = Hall.objects.get(id=hall_id)
    hall.delete()
    messages.success(request, f"{hall.name} has been deleted successfuly!")

    return redirect('list_halls')


# highest watched movie
@is_admin
def highest_watched_movie(request):
    movies = MovieSchedule.objects.all()
    highest_watched_movie = movies.order_by('-watched').first()
    context = {
        "highest_watched_movie": highest_watched_movie
    }

    return render(request, 'admin/highest_watched_movie.html', context)


# transaction_history
@is_admin
def transaction_history(request, customer_id):
    customer = CustomUser.objects.get(id=customer_id)
    transactions = Transaction.objects.filter(user=customer)
    #pagination
    paginator = Paginator(transactions, 7)
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)
    context = {
        "transactions": transactions,
        "customer": customer
    }

    return render(request, 'customer/transaction_history.html', context)