# Generated by Django 4.1 on 2023-01-01 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_transaction_discount_alter_transaction_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topup',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
