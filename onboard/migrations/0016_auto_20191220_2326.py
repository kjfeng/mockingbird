# Generated by Django 3.0 on 2019-12-21 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboard', '0015_auto_20191220_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='industry_match',
            field=models.CharField(choices=[('None', 'None'), ('Consulting', 'Consulting'), ('Finance', 'Finance'), ('Technology', 'Technology')], default='Industry 1', max_length=30),
        ),
    ]
