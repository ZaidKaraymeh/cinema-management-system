from django.shortcuts import render, redirect
from users.models import CustomUser
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import MovieForm
from .models import *

def home(request):
    user = CustomUser.objects.get(id=request.user.id)

    
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
