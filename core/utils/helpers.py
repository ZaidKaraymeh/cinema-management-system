from decimal import Decimal
import math as m
from ..models import *
def add_new_average(rating_average, count, value):
    avg = round(((count*rating_average) + value)/(count + 1), 1)
    #rounded = m.ceil(avg * 10) / 10
    #avg2 = rating_average + ((value - rating_average)/count)

    return Decimal(f'{avg}')

def subtract_new_average(rating_average, count, value):
    avg = round(((rating_average * count) - value) / (count - 1), 1)
    #rounded = m.ceil(avg * 10) / 10
    return Decimal(f'{avg}')
    
#avg = add_new_average(4.5, 2, 4)
#print(avg)
#print(subtract_new_average(4.3, 3, 4))


def get_time_slots(hall: Hall, date: str):
    timings = ['8:00', '11:00', '14:00', '17:00', '20:00', '23:00']

    for time in timings:
        slot, created = Slot.objects.get_or_create(
            slot=time,
            date_reserved=date
        )

    hall_slots = hall.slots.filter(date_reserved=date)
    slots = Slot.objects.filter(date_reserved=date)
    combined = []
    for x in hall_slots:
        combined.append(x)
    for x in slots:
        combined.append(x)

    unique_slots = [i for i in combined if combined.count(i) == 1]
    SLOT_CHOICES = [
        (
            str(slot.id),
            slot.slot
        ) for slot in unique_slots
    ]
    return SLOT_CHOICES

