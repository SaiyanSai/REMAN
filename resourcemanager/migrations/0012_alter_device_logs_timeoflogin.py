# Generated by Django 4.0.6 on 2023-04-03 23:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resourcemanager', '0011_alter_device_logs_dateoflogin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_logs',
            name='timeoflogin',
            field=models.TimeField(default=datetime.datetime(2023, 4, 3, 19, 33, 33, 633868)),
        ),
    ]
