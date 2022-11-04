from django.db import models
from users.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Venue(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    movies = models.ManyToManyField("core.Movie")

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)


class Hall(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    venue = models.ForeignKey("core.Venue", on_delete=models.CASCADE)

    seats = models.ManyToManyField("core.Seat")
    name = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)


class Movie(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    genres = models.ManyToManyField("core.Genre")

    name = models.CharField(max_length=255)

    """
        Calculate Average
        ((n)*old_average + new_rating )/(n+1)
        increment n
    """
    rating_average = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
    rating_count = models.IntegerField(default=0)
    reviews = models.ManyToManyField("core.Review")
    """
        Check if user found in users_rated, 
        if user not in users_rated, 
            call add_new_average
            increment rating_count
            update rating_average
        else:
            get old rating
            call subtract_new_average
            decrement rating_count
            update rating_average

            call add_new_average with new value
            increment rating_count
            update rating_average

    """

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)


class MovieSchedule(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    movie = models.ForeignKey("core.Movie", on_delete=models.CASCADE)
    hall = models.ForeignKey("core.Hall", on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=6, decimal_places=3)
    playtime = models.DateTimeField(auto_now=False, auto_now_add=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)


class Ticket(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_schedule = models.ForeignKey("core.MovieSchedule", on_delete=models.CASCADE)
    movie = models.ForeignKey("core.Movie", on_delete=models.CASCADE)
    hall = models.ForeignKey("core.Hall", on_delete=models.CASCADE)
    seat = models.ForeignKey("core.Seat", on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=6, decimal_places=3)
    playtime = models.DateTimeField(auto_now=False, auto_now_add=False)

    discount = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

class Seat(models.Model):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    hall = models.ForeignKey("core.Hall", on_delete=models.CASCADE)

    name = models.CharField(max_length=20)
    
    NORMAL = 'NRM'
    VIP = "VIP"
    SEAT_TYPE_CHOICES = [
        (NORMAL, "Normal"),
        (VIP, "VIP"),
    ]

    type = models.CharField(
        max_length=8,
        choices=SEAT_TYPE_CHOICES,
        default=NORMAL,

    )

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

class Balance(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=6, decimal_places=3)


    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

class Topup(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.ForeignKey("core.Balance", on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=6, decimal_places=3)
    is_approved = models.BooleanField()
    
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

class Review(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey("core.Movie", on_delete=models.CASCADE)

    rating = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
    comment = models.TextField(max_length=500, null=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

