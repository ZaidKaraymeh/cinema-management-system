# Generated by Django 4.1 on 2022-11-05 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_coupon_slot_remove_movieschedule_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movieschedule',
            name='playtime',
        ),
    ]