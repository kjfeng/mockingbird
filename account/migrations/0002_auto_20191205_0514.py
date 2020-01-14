# Generated by Django 2.2.6 on 2019-12-05 05:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='avg_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='late_num',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='tot_interview',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]