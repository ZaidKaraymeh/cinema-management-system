from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Movie)
admin.site.register(MovieSchedule)
admin.site.register(Ticket)
admin.site.register(Seat)
admin.site.register(Balance)
admin.site.register(Topup)
admin.site.register(Transaction)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Slot)
admin.site.register(Hall)