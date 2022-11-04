from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = f"{form.cleaned_data.get('first_name')}{form.cleaned_data.get('last_name')}"
            user.birth_date = form.cleaned_data['birth']

            user.save()
            messages.success(
                request, f"Your account has been created! You are now able to log in ")
            return redirect("login")

    else:

        form = RegisterForm()

    context = {"form": form}

    return render(request, "users/register.html", context)
