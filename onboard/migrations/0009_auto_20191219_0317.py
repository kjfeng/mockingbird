# Generated by Django 3.0 on 2019-12-19 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onboard', '0008_profile_match_filters'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='match_filters',
            new_name='filter_by',
        ),
    ]
