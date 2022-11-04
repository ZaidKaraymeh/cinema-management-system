from django.test import TestCase
from unittest import skip

# Create your tests here.

from .models import *
from .utils.helpers import subtract_new_average, add_new_average
from decimal import Decimal


class RatingTests(TestCase):

    def test_add_new_average(self):
        avg = 4.7
        count = 3
        value = 3
        expected_avg = Decimal('4.3')
        new_average = add_new_average(avg, count, value)
        self.assertEqual(expected_avg, new_average)
        self.assertIsInstance(new_average, Decimal)

    @skip("Skipped")
    def test_add_new_average_big_count(self):
        avg = 4.7
        count = 55
        value = 5
        expected_avg = Decimal('4.3')
        new_average = add_new_average(avg, count, value)
        self.assertEqual(expected_avg, new_average)
        self.assertIsInstance(new_average, Decimal)

    def test_add_new_average_from_zero(self):
        avg = 0
        count = 0
        value = 4
        avg1 = add_new_average(avg, count, value)
        count += 1
        value = 5
        avg2 = add_new_average(avg1, count, value)
        count += 1
        value = 5
        avg3 = add_new_average(avg2, count, value)

        expected_avg = Decimal('4.7')
        self.assertEqual(expected_avg, avg3)
        self.assertIsInstance(avg3, Decimal)

    def test_subtract_new_average(self):
        avg = 4.3
        count = 4
        value = 3
        expected_avg = Decimal('4.7')
        new_average = subtract_new_average(avg, count, value)
        self.assertEqual(expected_avg, new_average)
        self.assertIsInstance(new_average, Decimal)
