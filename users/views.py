from .forms import RegisterForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import json
# Create your views here.
from django.conf import settings
from users.models import CustomUser
from core.models import Balance, Transaction
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            messages.success(
                request, f"Your account has been created! You are now able to log in ")
            return redirect("login")

    else:
        form = RegisterForm()

    context = {"form": form}

    return render(request, "users/register.html", context)

# for AJAX login validation
# def login_ajax(request):
#     form = LoginForm(request.POST or None)
#     if form.is_valid():
#         # You could actually save through AJAX and return a success code here
#         form.save()
#         return HttpResponse(json.dumps({"success": True}))
#     return HttpResponse(json.dumps({'success': False}))


def profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    balance, created = Balance.objects.get_or_create(user=user)
    transactions = Transaction.objects.filter(user=user).order_by('-created_at')[:4]
    context = {
        "user":user,
        "balance":balance,
        "transactions":transactions
    }

    return render(request, "users/profile.html", context)