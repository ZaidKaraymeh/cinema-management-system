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
            print("form is valid")
            movie_schedule = schedule_form.save(commit=False)
            movie_schedule.slot = Slot.objects.get(
                id=slot_form['slots'].value()
            )
            hall = movie_schedule.hall.slots.add(movie_schedule.slot)
            movie_schedule.save()
            messages.success(
                request, f"{movie_schedule.movie.name} has been scheduled successfuly!")
            return redirect('list_schedule_movies')
        else:
            print("form is not valid")

    else:
        schedule_form = MovieScheduleForm(request.POST)
        slot_form = SlotForm()

    context = {
        'schedule_form': schedule_form,
        'slot_form': slot_form,
    }

    return render(request, 'admin/schedule_movie.html', context)


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