from django.shortcuts import render, redirect
from .models import Contact, feedback
from core.models import Balance
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from users.models import CustomUser
from payments.forms import TopUpForm
from payments.models import Topup
# from .forms import TopUpForm
# from .models import TopUpRequest

# def top_up(request):
#     if request.method == 'POST':
#         form = TopUpForm(request.POST)
#         if form.is_valid():
#             top_up_request = TopUpRequest(amount=form.cleaned_data['amount'], payment_method=form.cleaned_data['payment_method'], user=request.user)
#             top_up_request.save()
#             return redirect('top_up_success')
#     else:
#         form = TopUpForm()
#     return render(request, 'top_up.html', {'form': form})

# def top_up_success(request):
#     return render(request, 'top_up_success.html')

# def top_up_admin(request):
#     top_up_requests = TopUpRequest.objects.filter(approved=False)
#     return render(request, 'top_up_admin.html', {'top_up_requests': top_up_requests})

# def top_up_approve(request, top_up_request_id):
#     top_up_request = TopUpRequest.objects.get(id=top_up_request_id)
#     top_up_request.approved = True
#     top_up_request.save()
#     return redirect('top_up_admin')


# def ticket_confirmation(request, transaction_id):
#     return render(request, 'ticket_confirmation.html', {'transaction_id': transaction_id})

# def payment_successful(request):
#     return render(request, 'payment_successful.html')

# def userbalance(request):
#     if request.method=="POST":
#         id=request.POST.get('id') 
#         user=request.POST.get('user') 
#         balance=request.POST.get('balance') 
#         # amount=request.POST.get('amount')
#         print(id, user, balance)
#         user=Balance(id=id, user=user, balance=balance)
#         user.save()

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
    # return render(request, 'userbalance.html')

def topup(request): 
    user = CustomUser.objects.get(id=request.user.id)
    balance, created = Balance.objects.get_or_create(user=user)
    if request.method == "POST":
        topup_form = TopUpForm(request.POST)
        if topup_form.is_valid():
            obj = topup_form.save(commit=False)
            obj.balance = balance
            obj.user = user
            obj.save()
            messages.success(request, "Topup request sent")
            return redirect('home')
    else:
        topup_form = TopUpForm()
    
    context = {
        "topup_form": topup_form
    }


    return render(request, 'topUp.html', context)



def approve_topup(request, topup_id):
    topup = Topup.objects.get(id=topup_id)

    topup.is_approved = True
    topup.balance.balance += topup.amount
    topup.balance.save()
    topup.save()
    return redirect('list_topups')

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
        contact.save()
        if name and desc and phone and email:
            try:
                send_mail(name, 'Your contact form was submitted successfully',
                          'newtestingtest1@gmail.com', [email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/')
    else:
            return render(request, 'contact.html')

def contactFrom(request):
    return render(request, 'contactFrom.html')

def add_funds(request):
    user = request.user
    amount = request.POST.get('amount')
    # user.balance += amount
    user.save()
    return render(request, 'add_funds.html', {
        # 'user_balance': user.balance,
        'amount': amount,
    })

# def make_payment(request):
#     # retrieve user, amount, and payment method from request
#     user = request.user
#     amount = request.POST.get('amount')
#     payment_method = request.POST.get('payment_method')

#     if payment_method == 'credit_card':
#         pass
#     elif payment_method == 'paypal':
#         pass
#     else:
#         pass
#     # update user balance
#     # user.balance -= amount
#     user.save()
#     return render(request, 'make_payment.html', {
#         # 'user_balance': user.balance,
#         'amount': amount,
#         'payment_method': payment_method,
#     })





