# Generated by Django 2.2.6 on 2019-11-18 17:30

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('onboard', '0008_auto_20191117_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='industry',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Technology', 'Technology'), ('Finance', 'Finance'), ('Consulting', 'Consulting')], max_length=30),
        ),
    ]