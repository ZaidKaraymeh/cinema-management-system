from django.urls import path

from ..views import views
from ..views import admin_views
from ..views import customer_views


urlpatterns = [
    path('', views.home, name="home"),
] 
