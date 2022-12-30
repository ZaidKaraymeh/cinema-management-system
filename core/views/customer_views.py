from django.shortcuts import render, redirect
from ..models import Movie
from django.contrib import messages
from ..forms import *
from ..utils.helpers import *
from ..models import *

# Customer Movie Booking
def customer_movie_booking(request):
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
    return render(request, 'customer/movie_book.html')
