# Generated by Django 4.2.7 on 2023-12-19 01:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 19, 1, 51, 9, 226775, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
