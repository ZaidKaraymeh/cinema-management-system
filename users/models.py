from django.db import models
from django.contrib.auth.models import User as DjangoUser
# Create your models here.


class User(DjangoUser):
    CUSTOMER = 'CTM'
    ADMIN = "ADM"

    USER_TYPE_CHOICES = [
        (CUSTOMER, "Customer"),
        (ADMIN, "Admin"),
    ]

    phone_number = models.CharField(max_length=20, null=True)
    birth_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    user_type = models.CharField(
        max_length=8,
        choices=USER_TYPE_CHOICES,
        default=CUSTOMER,

    )
