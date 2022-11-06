# Generated by Django 4.1 on 2022-11-06 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='hall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.hall'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.movie'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='movie_schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.movieschedule'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.seat'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movieschedule',
            name='hall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.hall'),
        ),
        migrations.AddField(
            model_name='movieschedule',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.movie'),
        ),
        migrations.AddField(
            model_name='movieschedule',
            name='slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.slot'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(to='core.genre'),
        ),
        migrations.AddField(
            model_name='movie',
            name='reviews',
            field=models.ManyToManyField(to='core.review'),
        ),
        migrations.AddField(
            model_name='hall',
            name='seats',
            field=models.ManyToManyField(to='core.seat'),
        ),
        migrations.AddField(
            model_name='hall',
            name='slots',
            field=models.ManyToManyField(to='core.slot'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='discount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.coupon'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='movies',
            field=models.ManyToManyField(related_name='checkout_movies', to='core.movie'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='balance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
