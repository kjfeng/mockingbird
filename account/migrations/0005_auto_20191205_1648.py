# Generated by Django 2.2.6 on 2019-12-05 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20191205_1645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statistics',
            old_name='tot_num',
            new_name='tot_late',
        ),
    ]