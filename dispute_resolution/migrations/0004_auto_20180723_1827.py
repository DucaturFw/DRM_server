# Generated by Django 2.0.7 on 2018-07-23 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispute_resolution', '0003_auto_20180717_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractcase',
            name='finished',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Not finished'), (1, 'Pending'), (2, 'Finished')], default=0),
        ),
    ]
