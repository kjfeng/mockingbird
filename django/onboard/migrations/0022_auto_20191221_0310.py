# Generated by Django 3.0 on 2019-12-21 08:10

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('onboard', '0021_auto_20191221_0242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='filter_by',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Industry', 'Industry'), ('Role', 'Role'), ('Year In School', 'Year In School'), ('Similar Interviews', 'Similar # of Interviews'), ('Most Interviews', 'Most # Interviews'), ('Rating', 'Rating')], max_length=200),
        ),
    ]
