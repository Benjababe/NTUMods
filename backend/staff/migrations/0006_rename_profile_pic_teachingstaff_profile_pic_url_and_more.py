# Generated by Django 4.1.6 on 2023-02-27 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0005_teachingstaff_profile_pic_teachingstaff_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teachingstaff',
            old_name='profile_pic',
            new_name='profile_pic_url',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='interest',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
