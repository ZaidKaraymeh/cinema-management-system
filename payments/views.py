from django.shortcuts import render, redirect
from .models import Contact, feedback
from core.models import Balance, Ticket
# from .forms import PaymentMethod

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'ticket_detail.html', {'ticket': ticket})

def ticket_confirmation(request, transaction_id):
    return render(request, 'ticket_confirmation.html', {'transaction_id': transaction_id})

def payment_successful(request):
    return render(request, 'payment_successful.html')

def userbalance(request):
    if request.method=="POST":
        id=request.POST.get('id') 
        user=request.POST.get('user') 
        balance=request.POST.get('balance') 
        # amount=request.POST.get('amount')
        print(id, user, balance)
        user=Balance(id=id, user=user, balance=balance)
        user.save()

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

def add_funds(request):
    user = request.user
    amount = request.POST.get('amount')
    # user.balance += amount
    user.save()
    return render(request, 'add_funds.html', {
        # 'user_balance': user.balance,
        'amount': amount,
    })

def make_payment(request):
    # retrieve user, amount, and payment method from request
    user = request.user
    amount = request.POST.get('amount')
    payment_method = request.POST.get('payment_method')

    if payment_method == 'credit_card':
        pass
    elif payment_method == 'paypal':
        pass
    else:
        pass
    # update user balance
    # user.balance -= amount
    user.save()
    return render(request, 'make_payment.html', {
        # 'user_balance': user.balance,
        'amount': amount,
        'payment_method': payment_method,
    })





