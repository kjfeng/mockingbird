# Generated by Django 2.2.7 on 2019-12-06 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboard', '0016_remove_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_sender',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='time_matched',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
