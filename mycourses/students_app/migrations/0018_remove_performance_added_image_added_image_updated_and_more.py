# Generated by Django 5.0.6 on 2024-05-21 12:07

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_app', '0017_image_title_alter_performance_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='added',
        ),
        migrations.AddField(
            model_name='image',
            name='added',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='added',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='date_of_mark',
            field=models.DateField(default=datetime.datetime(2024, 5, 21, 12, 6, 49, 78882, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='performance',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='student',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
