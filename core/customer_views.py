from django.shortcuts import render, redirect
from users.models import CustomUser
from .models import Movie
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import *
from .utils.helpers import *
from .models import *
import json
from django.http import HttpResponse
