# Generated by Django 2.2.6 on 2020-01-07 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboard', '0031_profile_requested_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='requested_name',
            field=models.CharField(default='', max_length=500),
        ),
    ]
