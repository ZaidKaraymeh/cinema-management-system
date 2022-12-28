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


def home(request):
    user = request.user

    # last 10 records of movies
    movies_featured = Movie.objects.all().reverse()[:3]
    movies = Movie.objects.all()

    context = {
        'movies':movies_featured,
        'movies_list': movies
    }

    return render(request, "home.html", context)


def movie_details(request, movie_id):
    # try:
    #     movie = Movie.objects.get(id=movie_id)
    #     context = {
    #         'movie':movie
    #     }

    #     return render(request, 'customer/movie_details.html', context)
    # except:
    #     return redirect('home')
    movie = Movie.objects.get(id=movie_id)
    movie_schedules = MovieSchedule.objects.filter(movie=movie)
    context = {
        'movie':movie,
        "movie_schedules": movie_schedules
    }

    return render(request, 'customer/movie_details.html', context)






    
