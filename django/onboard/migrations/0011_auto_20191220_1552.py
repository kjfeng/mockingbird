# Generated by Django 3.0 on 2019-12-20 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboard', '0010_auto_20191220_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='industry',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='industry1',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='industry2',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='industry3',
        ),
        migrations.AddField(
            model_name='profile',
            name='industry_choice_1',
            field=models.CharField(choices=[('Technology', 'Technology'), ('Finance', 'Finance'), ('Consulting', 'Consulting'), ('None', 'None')], default='None', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='industry_choice_2',
            field=models.CharField(choices=[('Technology', 'Technology'), ('Finance', 'Finance'), ('Consulting', 'Consulting'), ('None', 'None')], default='None', max_length=30),
            preserve_default=False,
        ),
    ]
