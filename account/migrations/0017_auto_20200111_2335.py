# Generated by Django 2.2.6 on 2020-01-12 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20200109_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationitem',
            name='type',
            field=models.CharField(choices=[('MR', 'Match Request'), ('CS', 'Complete Survey'), ('MC', 'Match Canceled'), ('MA', 'Match Accept'), ('MD', 'Match Deny/Reject'), ('DA', 'Deleted Account'), ('DAR', 'Deleted Account Request')], max_length=100),
        ),
    ]