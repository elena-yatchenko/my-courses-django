# Generated by Django 5.0.4 on 2024-05-11 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_app', '0006_alter_course_options_alter_course_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='marks',
            field=models.ManyToManyField(blank=True, to='students_app.mark'),
        ),
    ]
