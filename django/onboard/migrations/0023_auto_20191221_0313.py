# Generated by Django 3.0 on 2019-12-21 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onboard', '0022_auto_20191221_0310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='filter_by',
            new_name='rank_by',
        ),
    ]
