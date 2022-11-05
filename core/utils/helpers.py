from decimal import Decimal
import math as m

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