# Generated by Django 5.0.4 on 2024-05-18 19:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_app', '0010_alter_review_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='added',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
