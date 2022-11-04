from django.shortcuts import render, redirect
from users.models import CustomUser
from django.contrib import messages
# Create your views here.

from .forms import MovieForm
from .models import *

def home(request):
    user = CustomUser.objects.get(id=request.user.id)

    
    return render(request, "admin_home.html")



def list_movies(request):
    movies = Movie.objects.all()
    context = {
        "movies": movies,
    }

    return render(request, 'list_movies.html', context)


def add_movie(request):
    user = CustomUser.objects.get(id=request.user.id)
   
    if request.method == "POST":
        movie_form = MovieForm(request.POST)
        if movie_form.is_valid():
            movie = movie_form.save()
            messages.success(request, f"{movie.name} has been added successfuly!")
            return redirect('add_movie')
    else:
        movie_form = MovieForm()

    context = {
        "movie_form": movie_form,
    }
    return render(request, "add_movie.html", context)