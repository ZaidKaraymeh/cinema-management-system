from django.http import HttpResponse
from django.shortcuts import render, redirect
from ..models import Movie
from django.contrib import messages
from ..forms import *
from ..utils.helpers import *
from ..models import *
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse

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

# @api_view(['POST'])
@csrf_exempt
def book_ticket_json(request, schedule_id, user_id):
    user = CustomUser.objects.get(id=user_id)
    movie_schedule = MovieSchedule.objects.get(id=schedule_id)
    balance, created = Balance.objects.get_or_create(user=user)

    data = json.loads(request.body)

    total = 0
    for item in data:
        seat = Seat.objects.get(id=item['id'])
        if seat.type == "VIP":
            total += Decimal(4.5)
        else:
            total += Decimal(3.0)
    # balance.balance = Decimal(100)
    if total > balance.balance:
        return JsonResponse({'error': 'Insufficient Balance'})
    
    transaction = Transaction.objects.create(
        user=user,
    )
    transaction.save()
    for item in data:
        seat = Seat.objects.get(id=item['id'])
        ticket = Ticket.objects.create(
            user=user,
            movie_schedule=movie_schedule,
            seat = seat,
            price = Decimal(3) if seat.type == "VIP" else Decimal(4.5)
        )
        ticket.save()
        transaction.tickets.add(ticket)

    transaction.amount = Decimal(total)
    balance.balance -= total
    balance.save()
    transaction.isPaid = True

    return JsonResponse({'code': '200', 'balance': balance.balance})

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
