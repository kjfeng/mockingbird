# Generated by Django 2.2.6 on 2019-12-22 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20191220_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationitem',
            name='type',
            field=models.CharField(choices=[('MR', 'Match Request'), ('CS', 'Complete Survey'), ('MC', 'Match Canceled')], default='MR', max_length=100),
            preserve_default=False,
        ),
    ]
