# Generated by Django 2.2.6 on 2019-12-09 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onboard', '0003_auto_20191208_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone',
        ),
    ]
