from django.shortcuts import render

def payment_successful(request):
    return render(request, 'payment_successful.html')

def balance(request):
    return render(request, 'balance.html')

def topUp(request):
    return render(request, 'topUp.html')

def checkout(request):
    return render(request, 'checkout.html')

def userfeedback(request):
    return render(request, 'userfeedback.html')

def contactUs(request):
    return render(request, 'contactUs.html')