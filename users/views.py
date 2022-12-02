from .forms import RegisterForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.http import HttpResponse
import json
# Create your views here.
from django.conf import settings
User = settings.AUTH_USER_MODEL

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Your account has been created! You are now able to log in ")
            return redirect("login")

    else:
        form = RegisterForm()

    context = {"form": form}

    return render(request, "users/register.html", context)

# for AJAX login validation
def login_ajax(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        # You could actually save through AJAX and return a success code here
        form.save()
        return HttpResponse(json.dumps({"success": True}))
    return HttpResponse(json.dumps({'success': False}))