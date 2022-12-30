from time import time
from django import template
from django.utils import timezone

register = template.Library()


def in_row(queryset, counter):
    return queryset[8 * (counter - 1):(counter * 8)]

"""
    0 - 7 # 7 = 1 * 8 - 1
    8 - 15 # 15 = 2 * 8 - 1
    16 - 23 # 23 = 3 * 8 - 1
    24 - 31
    32 - 39
    40 - 47
"""





register.filter('in_row', in_row)

