# Generated by Django 2.2.6 on 2020-01-12 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_merge_20200112_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationitem',
            name='type',
            field=models.CharField(choices=[('MR', 'Match Request'), ('MC', 'Match Canceled'), ('MA', 'Match Accept'), ('MD', 'Match Deny/Reject'), ('DA', 'Deleted Account'), ('DAR', 'Deleted Account Request')], max_length=100),
        ),
    ]