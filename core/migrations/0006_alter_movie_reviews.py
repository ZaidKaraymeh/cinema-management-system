# Generated by Django 4.1 on 2022-12-09 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_slot_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='reviews',
            field=models.ManyToManyField(blank=True, to='core.review'),
        ),
    ]