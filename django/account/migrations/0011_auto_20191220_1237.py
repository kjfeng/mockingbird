# Generated by Django 2.2.6 on 2019-12-20 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20191220_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]