from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views
from users import views as user_views
from payments import views as payments_views


from django.conf import settings
from django.conf.urls.static import static

from users.forms import LoginForm

urlpatterns = [
    path('topup/', payments_views.topup, name="topup" ),   
    path('topup/approve/<str:topup_id>', payments_views.approve_topup, name="approve_topup" ),   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

