# Generated by Django 2.2.6 on 2019-12-09 02:57

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('onboard', '0002_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=phone_field.models.PhoneField(blank=True, default='(None)', help_text='Contact phone number', max_length=31),
        ),
    ]
