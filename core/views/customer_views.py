from django.shortcuts import render, redirect
from ..models import Movie
from django.contrib import messages
from ..forms import *
from ..utils.helpers import *
from ..models import *

# Customer Movie Booking
def customer_movie_booking(request, schedule_id):
    movie_schedule = MovieSchedule.objects.get(id=schedule_id)
    ordered_seats = movie_schedule.hall.seats.all().order_by('name')
    balance, created = Balance.objects.get_or_create(user=request.user)

    context = {
        'movie_schedule': movie_schedule,
        'ordered_seats': ordered_seats,
        'balance': balance
    }


    return render(request, 'customer/movie_book.html', context)



#def customer_movie_booking(request, movie_id):
    # movie = Movie.objects.get(id=movie_id)
    # if request.method == 'POST':
    #     #form = BookingForm(request.POST)
    #     if form.is_valid():
    #         booking = form.save(commit=False)
    #         booking.user = request.user
    #         booking.movie = movie
    #         booking.save()
    #         messages.success(request, 'Booking Successful')
    #         return redirect('customer-movie-booking', movie_id=movie_id)
    # else:
    #     #form = BookingForm()
    #     pass
    # context = {
    #     'form': form,
    #     'movie': movie
    # }
    #return render(request, 'customer/movie_booking.html', context)
