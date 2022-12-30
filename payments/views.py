from django.shortcuts import render, redirect
from .models import Contact, feedback
# from .forms import TicketPurchaseForm
# from .forms import balance

# from .forms import TicketForm
from .forms import PaymentMethod
from .backend import process_payment

def purchase_ticket(request):
    # if request.method == 'POST':
    #     form = TicketForm(request.POST)
    #     if form.is_valid():
    #         # Process the payment
    #         amount = form.cleaned_data['price']
    #         transaction_id = process_payment(amount)
    #         form.save()
    #         # Create a fake payment transaction
    #         transaction_id = '12345'
    #         form.save()
    #         return redirect('ticket_confirmation', transaction_id)
    # else:
    #     form = TicketForm()
    return render(request, 'purchase_ticket.html')

def ticket_confirmation(request, transaction_id):
    return render(request, 'ticket_confirmation.html', {'transaction_id': transaction_id})

def payment_successful(request):
    return render(request, 'payment_successful.html')

def userbalance(request):
    # # retrieve user and amount from request
    # user = request.user
    # amount = request.POST.get('amount')

    # # update user balance
    # # user.balance += amount
    # user.save()

    # # render response
    # return render(request, 'userbalance.html', {
    #     # 'user_balance': user.balance,
    #     'amount': amount,
    # })
    # # if request.method == 'POST':
    #     # form = PaymentMethod(request.POST)
    return render(request, 'userbalance.html')

def topUp(request):
    return render(request, 'topUp.html')

def checkout(request):
    return render(request, 'checkout.html')

def userfeedback(request):
    if request.method=="POST":
        fname=request.POST.get('fname') 
        lname=request.POST.get('lname') 
        email=request.POST.get('email') 
        point1=request.POST.get('point1')
        point2=request.POST.get('point2')
        point3=request.POST.get('point3')
        point4=request.POST.get('point4')
        point5=request.POST.get('point5')
        comment=request.POST.get('comment')
        print(fname, lname, email, point1, point2, point3, point4, point5, comment)
        feed=feedback(fname=fname,lname=lname, email=email, point1=point1, point2=point2, point3=point3, point4=point4, point5=point5, comment=comment)
        feed.save()
    return render(request, 'userfeedback.html')


def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        print (name, email, phone, desc)
        contact=Contact(name=name, email=email, phone=phone, desc=desc)
        # Contact.objects.create(name=name, email=email, phone=phone, decs=desc)      
        contact.save()
    return render(request, 'contact.html')

def book_ticket(request):
    return render(request, 'book_ticket.html')


def add_funds(request):
    # retrieve user and amount from request
    user = request.user
    amount = request.POST.get('amount')

    # update user balance
    # user.balance += amount
    user.save()

    # render response
    return render(request, 'add_funds.html', {
        # 'user_balance': user.balance,
        'amount': amount,
    })

def make_payment(request):
    # retrieve user, amount, and payment method from request
    user = request.user
    amount = request.POST.get('amount')
    payment_method = request.POST.get('payment_method')

    # make payment
    if payment_method == 'credit_card':
        # make payment using credit card
        pass
    elif payment_method == 'paypal':
        # make payment using PayPal
        pass
    else:
        # invalid payment method
        pass

    # update user balance
    # user.balance -= amount
    user.save()

    # render response
    return render(request, 'make_payment.html', {
        # 'user_balance': user.balance,
        'amount': amount,
        'payment_method': payment_method,
    })





