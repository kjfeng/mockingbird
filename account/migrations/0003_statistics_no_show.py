# Generated by Django 2.2.6 on 2019-12-05 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20191205_0514'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='no_show',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
