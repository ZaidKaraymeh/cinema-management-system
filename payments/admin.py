from django.contrib import admin

# Register your models here.
from .models import Contact, feedback, Topup
admin.site.register(Contact)
admin.site.register(feedback)
admin.site.register(Topup)
