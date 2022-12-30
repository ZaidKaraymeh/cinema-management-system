"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views
from users import views as user_views
from payments import views as payments_views


from django.conf import settings
from django.conf.urls.static import static

from users.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html", form_class=LoginForm), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path('register/', user_views.register, name="register"),
    # path('login_ajax/', user_views.login_ajax, name="login_ajax"),
    path('userbalance/', payments_views.userbalance, name="userbalance" ),
    path('payment_successful/', payments_views.payment_successful, name="payment_successful" ), 
    path('topUp/', payments_views.topUp, name="topUp" ),   
    path('checkout/', payments_views.checkout, name="checkout" ), 
    path('userfeedback/', payments_views.userfeedback, name="userfeedback" ),
    path('contact/', payments_views.contact, name="contact" ),
    path('', include('django_prometheus.urls')),
    path('purchase_ticket/', payments_views.purchase_ticket, name="purchase_ticket" ),
    path('add_funds/', payments_views.add_funds, name="add_funds" ),
    path('make_payment/', payments_views.make_payment, name="make_payment" ),


    
    path('', include('core.urls.urls')),
    path('', include('core.urls.admin_urls')),
    #path('profile/', user_views.profile, name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

