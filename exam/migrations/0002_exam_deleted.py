# Generated by Django 4.2.7 on 2024-05-22 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
