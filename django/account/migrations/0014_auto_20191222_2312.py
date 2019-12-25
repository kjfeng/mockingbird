# Generated by Django 2.2.6 on 2019-12-23 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_notificationitem_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationitem',
            name='type',
            field=models.CharField(choices=[('MR', 'Match Request'), ('CS', 'Complete Survey'), ('MC', 'Match Canceled'), ('MA', 'Match Accept'), ('MD', 'Match Deny/Reject')], max_length=100),
        ),
    ]