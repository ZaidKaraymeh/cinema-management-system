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


def dashboard(request):

    return render(request, 'admin/dashboard.html')



def list_movies(request):
    list_movies = Movie.objects.all().order_by('created_at')

    paginator = Paginator(list_movies, 10)
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)

    context = {
        "movies": movies,
    }

    return render(request, 'admin/movies.html', context)

@staff_member_required()
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


def edit_movie(request, movie_id):
    user = request.user
    movie = Movie.objects.get(id=movie_id)

    if request.method == "POST":
        movie_form = MovieForm(request.POST, instance=movie)
        if movie_form.is_valid():
            movie = movie_form.save(commit=False)
            movie.save()
            messages.info(
                request, f"{movie.title} has been Edited successfuly!")
            return redirect('list_movies')
    else:
        movie_form = MovieForm(instance=movie)

    context = {
        "form": movie_form,
        "movie": movie,
    }
    return render(request, "admin/edit_movie.html", context)


def delete_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.delete()
    messages.error(request, f"{movie.title} has been Deleted successfuly!")

    return redirect('list_movies')


def list_schedule_movies(request):
    movie_schedules = MovieSchedule.objects.all()

    paginator = Paginator(movie_schedules, 10)
    page_number = request.GET.get('page')
    movie_schedules = paginator.get_page(page_number)

    context = {
        'movie_schedules': movie_schedules
    }

    return render(request, 'admin/list_movies_scheduled.html', context)


def schedule_movie(request):
    if request.method == "POST":
        schedule_form = MovieScheduleForm(request.POST)
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
        schedule_form = MovieScheduleForm(request.POST)
        slot_form = SlotForm()

    context = {
        'schedule_form': schedule_form,
        'slot_form': slot_form,
    }

    return render(request, 'admin/schedule_movie.html', context)

#edit schedule movie
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


def delete_movie_schedule(request, schedule_id):
    schedule = MovieSchedule.objects.get(id=schedule_id)
    schedule.delete()
    messages.error(request, f"{schedule.movie.title} has been Deleted successfuly!")

    return redirect('list_schedule_movies')

# delete hall
def delete_hall(request, hall_id):
    hall = Hall.objects.get(id=hall_id)
    hall.delete()
    messages.error(request, f"{hall.name} has been Deleted successfuly!")

    return redirect('list_halls')

def slots_available_json(request, hall_id, date):
    hall = Hall.objects.get(id=hall_id)

    slot_choices = get_time_slots(hall, date)

    response = json.dumps(dict(slot_choices))

    return HttpResponse(response)

def list_customers(request):
    customers = CustomUser.objects.filter(user_type='CTM')
    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    customers = paginator.get_page(page_number)

    context = {
        'customers': customers,
    }
    return render(request, 'admin/list_customers.html', context)

def list_employees(request):
    employees = CustomUser.objects.filter(user_type='ADM')
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    employees = paginator.get_page(page_number)

    context = {
        'employees': employees,
    }
    return render(request, 'admin/list_employees.html', context)

# Todo 
def view_customer_ticket_history(request):
    pass


def list_halls(request):

    halls = Hall.objects.all()
    paginator = Paginator(halls, 10)
    page_number = request.GET.get('page')
    halls = paginator.get_page(page_number)

    context = {
        'halls': halls,
    }

    return render(request, 'admin/list_halls.html', context)

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
