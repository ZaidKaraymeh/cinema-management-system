from decimal import Decimal
from django.db import models
from users.models import CustomUser
from django.conf import settings
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
import datetime


# class Venue(models.Model):
#     id = models.UUIDField(
#         primary_key=True, default=uuid.uuid4, editable=False, unique=True)
#     name = models.CharField(max_length=20)
#     address = models.CharField(max_length=255)
#     movies = models.ManyToManyField("core.Movie")

#     created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
#     modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)


class Hall(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    #venue = models.ForeignKey("core.Venue", on_delete=models.CASCADE)

    seats = models.ManyToManyField("core.Seat", blank=True)
    slots = models.ManyToManyField("core.Slot", blank=True)

    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __str__(self) -> str:
        return str(self.name)

class Slot(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    # _id = models.IntegerField()

    EIGHT_AM = '8:00'
    ELEVEN_AM = "11:00"
    TWO_PM = '14:00'
    FIVE_PM = '17:00'
    EIGHT_PM = '20:00'
    ELEVEN_PM = '23:00'
    SLOT_TIME_CHOICES = [
        (EIGHT_AM, "8:00"),
        (ELEVEN_AM, "11:00"),
        (TWO_PM, "14:00"),
        (FIVE_PM, "17:00"),
        (EIGHT_PM, "20:00"),
        (ELEVEN_PM, "23:00"),
    ]

    slot = models.CharField(
        max_length=8,
        choices=SLOT_TIME_CHOICES,
        default=EIGHT_AM,

    )

    date_reserved = models.DateField(
        auto_now_add=False, auto_now=False, default=datetime.date.today)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)


    """ def save(self, *args, **kwargs):
        self.object_list = Slot.objects.order_by('_id')
        if len(self.object_list) == 0:  # if there are no objects
            self._id = 1
        else:
            self._id = self.object_list.last()._id + 1
        super(Slot, self).save() """

    def __str__(self) -> str:
        return str(self.slot)

class Movie(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    trailer = models.FileField(upload_to='movies', max_length=100, null=True)
    thumbnail = models.FileField(
        upload_to='thumbnail', max_length=100, null=False, default='undefined')

    release_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True)
    duration = models.CharField(max_length=4, default="60")
    genres = models.ManyToManyField("core.Genre")
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1500, null=True)

    RUNNING = 'Running'
    UPCOMING = "Upcoming"
    ARCHIVED = "Archived"
    STATUS_TYPE_CHOICES = [
        (RUNNING, "Running"),
        (UPCOMING, "Upcoming"),
        (ARCHIVED, "Archived"),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_TYPE_CHOICES,
        default=ARCHIVED,

    )
    
    """
        Calculate Average
        ((n)*old_average + new_rating )/(n+1)
        increment n
    """
    # rating_average = models.DecimalField(
    #     default=Decimal(0), max_digits=2, decimal_places=1,
    #     validators=[
    #         MaxValueValidator(5),
    #         MinValueValidator(0)
    #     ])
    # rating_count = models.IntegerField(default=0)
    # reviews = models.ManyToManyField("core.Review", blank=True)
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

    def __str__(self):
        return str(self.title)


# schedule.hall.seats.all()
class MovieSchedule(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    movie = models.ForeignKey(
        "core.Movie", on_delete=models.CASCADE, blank=True)
    hall = models.ForeignKey("core.Hall", on_delete=models.CASCADE, blank=True)
    slot = models.ForeignKey("core.Slot", on_delete=models.CASCADE, null=True)
    reserved_seats = models.ManyToManyField("core.Seat", blank=True)
    selected_seats = models.ManyToManyField(
        "core.Seat", blank=True, related_name="selected_seats")
    #playtime = models.DateTimeField(auto_now=False, auto_now_add=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.id)


class Ticket(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie_schedule = models.ForeignKey(
        "core.MovieSchedule", on_delete=models.CASCADE)
    seat = models.ForeignKey("core.Seat", on_delete=models.CASCADE, null=True)

    price = models.DecimalField(
        max_digits=6, decimal_places=3, default=Decimal(0))

    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    # @property
    # def get_price(self):
    #     # type: ignore
    #     return Decimal(3) if self.seat.type == "NRM" else Decimal(4.5)

    def __str__(self):
        return str(self.id)


class Seat(models.Model):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    #hall = models.ForeignKey("core.Hall", on_delete=models.CASCADE)
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(
        max_digits=6, decimal_places=3, default=Decimal('0'))

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    # def __str__(self):
    #     return f"{self.user.email}  {self.balance}"
    
    def __str__(self):
        return str(self.balance)


class Transaction(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=6, decimal_places=3, default=Decimal('0'))

    tickets = models.ManyToManyField("core.Ticket")

    # If the user paid online or in person
    isPaid = models.BooleanField(default=False)

    # BENEFIT = 'BNF'
    # PAYPAL = "PAL"
    # CREDIT_CARD = "CRC"
    # PAYMENT_TYPE_CHOICES = [
    #     (BENEFIT, "Benefit"),
    #     (PAYPAL, "Paypal"),
    #     (CREDIT_CARD, "Credit Card"),
    # ]

    # payment_type = models.CharField(
    #     max_length=15,
    #     choices=PAYMENT_TYPE_CHOICES,
    #     default=BENEFIT,
    # )

    # discount =  models.ForeignKey("core.Coupon", on_delete=models.CASCADE)

    # @property
    # def final_price(self):
    #     """
    #         VIP tickets are 1.5 more than normal tickets from Decimal(1.5)
    #     """

    #     final : Decimal = Decimal('0')

    #     for movie in self.movies.all():

    #         if movie.seat.type == "VIP":
    #             final += movie.price - movie.price * Decimal(self.discount.discount/100) * Decimal(1.5)
    #         else:
    #             final += movie.price - movie.price * Decimal(self.discount.discount/100)

    #     return round(final, 3)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.amount)

# class Review(models.Model):
#     id = models.UUIDField(
#         primary_key=True, default=uuid.uuid4, editable=False, unique=True)

#     user = models.ForeignKey(CustomUser,
#                              on_delete=models.CASCADE)
#     #movie = models.ForeignKey("core.Movie", on_delete=models.CASCADE)

#     rating = models.IntegerField(
#         validators=[
#             MaxValueValidator(5),
#             MinValueValidator(0)
#         ])
#     comment = models.TextField(max_length=500, null=True)

#     created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
#     modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

#     def __str__(self):
#         return str(self.id)

class Genre(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    name = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.name)


# class Coupon(models.Model):
#     id = models.UUIDField(
#         primary_key=True, default=uuid.uuid4, editable=False, unique=True)

#     code = models.CharField(max_length=20)
#     discount = models.IntegerField(
#         default=0,
#         validators=[
#             MaxValueValidator(100),
#             MinValueValidator(0)
#         ])
#     count = models.IntegerField(default=0)
#     ends_at = models.DateTimeField(auto_now_add=False, auto_now=False)
#     created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
#     modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)
