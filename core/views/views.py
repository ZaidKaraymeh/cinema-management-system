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




def book_movie_seat_availability(request, schedule_id):
    data = json.loads(request.body)
    movie_schedule = MovieSchedule.objects.get(id=schedule_id)
    selected_seats = data['selectedSeats']

    for seat in selected_seats:
        if seat in movie_schedule.reserved_seats.all():
            return HttpResponse(json.dumps({'status': 'error', 'message': 'Seat already reserved'}), status_code=400)
    

    for seat_id in selected_seats:
        movie_schedule.selected_seats.add(seat_id)

    movie_schedule.save()
    
    return HttpResponse(json.dumps({'status': 'success'}), status_code=200) 



def book_movie_json(request, schedule_id, user_id):
    data = json.loads(request.body)

    user = CustomUser.objects.get(id=user_id)
    movie_schedule = MovieSchedule.objects.get(id=schedule_id)

    for seat in data['seats']:
        ticket = Ticket.objects.create(
            user=user,
            movie_schedule=movie_schedule,
            seat=seat,
            price=movie_schedule.movie.price,
            playtime=movie_schedule.slot
        )

    #response = json.dumps(dict(slot_choices))

    #return HttpResponse(response)
