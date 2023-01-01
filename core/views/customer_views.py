from payments.models import Topup
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
from django.db import transaction
from django.core.mail import send_mail
from django.template import loader


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
@transaction.atomic
def book_ticket_json(request, schedule_id, user_id):
    user = CustomUser.objects.get(id=user_id)
    movie_schedule = MovieSchedule.objects.get(id=schedule_id)
    balance, created = Balance.objects.get_or_create(user=user)

    data = json.loads(request.body)

    total = 0
    for item in data['seats']:
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
    for item in data['seats']:
        seat = Seat.objects.get(id=item['id'])
        ticket = Ticket.objects.create(
            user=user,
            movie_schedule=movie_schedule,
            seat = seat,
            price = Decimal(3) if seat.type == "VIP" else Decimal(4.5)
        )
        ticket.save()
        transaction.tickets.add(ticket)
        movie_schedule.reserved_seats.add(seat)

    transaction.amount = Decimal(total)
    transaction.save()
    balance.balance -= total
    balance.save()

    if data['isOnline']:
        transaction.isPaid = True
        transaction.save()
    html_message = loader.render_to_string(
        'customer/email.html',
        {
            'user': user,
            'transaction':  transaction,
            "site": "http://127.0.0.1:8000"
        }
    )
    send_mail(
        f"Purchase Transaction ID: {transaction.id}", 
        'Your contact form was submitted successfully',
        'cinema.admin.bh@gmail.com', 
        [f'{user.email}'],
        fail_silently=False,
        html_message=html_message,
        )


    return JsonResponse({'code': '200', 'balance': balance.balance})

#def tickets(request, transaction_id):
def tickets(request):
    # transaction = Transaction.objects.get(id=transaction_id)
    # context = {
    #     'transaction': transaction
    # }
    #return render(request, 'customer/tickets.html', context)
    return render(request, 'customer/tickets.html')
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

# view transaction histor
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    context = {
        'transactions': transactions
    }
    return render(request, 'customer/transaction_history.html', context)

# topup history
def topup_history(request):
    topups = Topup.objects.filter(user=request.user)
    context = {
        'topups': topups
    }
    return render(request, 'customer/topup_history.html', context)