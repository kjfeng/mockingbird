# Generated by Django 2.2.6 on 2019-12-20 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20191220_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationitem',
            name='read_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]