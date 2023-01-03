# Generated by Django 4.1 on 2022-12-31 17:50

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_ticket_seats_ticket_seat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='discount',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=3, default=Decimal('0'), max_digits=6),
        ),
        migrations.DeleteModel(
            name='Coupon',
        ),
    ]
