# Generated by Django 4.1.6 on 2023-02-25 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_module', '0001_initial'),
        ('timeslot', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='timeslot',
            unique_together={('index', 'group', 'day', 'time_start',
                              'time_end', 'semester', 'year', 'module')},
        ),
    ]
