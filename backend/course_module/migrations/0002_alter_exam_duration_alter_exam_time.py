# Generated by Django 4.1.6 on 2023-02-25 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='duration',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='time',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
