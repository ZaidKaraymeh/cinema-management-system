# Generated by Django 4.1 on 2022-12-31 17:44

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_transaction_movies_transaction_ispaid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='playtime',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='seat',
        ),
        migrations.AddField(
            model_name='ticket',
            name='seats',
            field=models.ManyToManyField(blank=True, to='core.seat'),
        ),
        migrations.AlterField(
            model_name='balance',
            name='balance',
            field=models.DecimalField(decimal_places=3, default=Decimal('0'), max_digits=6),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.DecimalField(decimal_places=3, default=Decimal('0'), max_digits=6),
        ),
    ]