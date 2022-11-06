from django.shortcuts import render, redirect
from users.models import CustomUser
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import *
from .utils.helpers import *
from .models import *
import json
from django.http import HttpResponse
def home(request):
    user = CustomUser.objects.get(id=request.user)

    
    return render(request, "admin_home.html")



def list_movies(request):
    list_movies = Movie.objects.all()

    paginator = Paginator(list_movies, 10)
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)

    context = {
        "movies": movies,
    }

    return render(request, 'list_movies.html', context)


def add_movie(request):
    user = CustomUser.objects.get(id=request.user.id)
   
    if request.method == "POST":
        movie_form = MovieForm(request.POST)
        if movie_form.is_valid():
            movie = movie_form.save(commit=False)
            movie.save()
            messages.success(request, f"{movie.name} has been added successfuly!")
            return redirect('list_movies')
    else:
        movie_form = MovieForm()

    context = {
        "movie_form": movie_form,
    }
    return render(request, "add_movie.html", context)

def edit_movie(request, movie_id):
    user = CustomUser.objects.get(id=request.user.id)
    movie = Movie.objects.get(id=movie_id)

    if request.method == "POST":
        movie_form = MovieForm(request.POST, instance=movie)
        if movie_form.is_valid():
            movie = movie_form.save(commit=False)
            movie.save()
            messages.info(request, f"{movie.name} has been Edited successfuly!")
            return redirect('list_movies')
    else:
        movie_form = MovieForm(instance=movie)

    context = {
        "movie_form": movie_form,
    }
    return render(request, "edit_movie.html", context)

def delete_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.delete()
    messages.error(request, f"{movie.name} has been Deleted successfuly!")

    return redirect('list_movies')


def schedule_movie(request):
    
    if request.method == "POST":
        schedule_form = MovieScheduleForm(request.POST)
        if schedule_form.is_valid():
            movie_schedule = schedule_form.save(commit=False)
            movie_schedule.slot = schedule_form.cleaned_data['slots']
            movie_schedule.save()
            messages.success(request, f"{movie_schedule.movie.name} has been scheduled successfuly!")
            return redirect('list_movies')
    else:
        schedule_form = MovieScheduleForm(request.POST)
    
    context = {
        'schedule_form': schedule_form
    }

    return render(request, 'schedule_movie.html', context)



def slots_available_json(request, hall_id):
    hall = Hall.objects.get(id=hall_id)

    slot_choices = get_time_slots(hall)
    
    response = json.dumps(dict(slot_choices))

    return HttpResponse(response)
    
