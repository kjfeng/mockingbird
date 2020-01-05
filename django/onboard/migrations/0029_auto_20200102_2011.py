# Generated by Django 2.2.6 on 2020-01-03 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboard', '0028_profile_is_idle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='industry_match',
            field=models.CharField(choices=[('Industry 1', 'Industry 1'), ('Industry 2', 'Industry 2'), ('Both', 'Both')], default='Industry 1', max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_idle',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
    ]
