from django.db import models
# from django.contrib.auth.models import User
import uuid
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")
    # timeStamp =models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

class feedback(models.Model):
    sno = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=70)
    point1 = models.CharField(max_length=70)
    point2 = models.CharField(max_length=70)
    point3 = models.CharField(max_length=70)
    point4 = models.CharField(max_length=70)
    point5 = models.CharField(max_length=70)
    comment = models.CharField(max_length=1000)


# class TopUpRequest(models.Model):
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_method = models.CharField(max_length=50)
#     # user = models.ForeignKey(User, on_delete=models.CASCADE)
#     approved = models.BooleanField(default=False)




class Topup(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance = models.ForeignKey("core.Balance", on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=6, decimal_places=3, validators=[MinValueValidator(Decimal('1')), MaxValueValidator(Decimal('25'))])
    is_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)
