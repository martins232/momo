# Generated by Django 4.2.7 on 2024-03-03 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0006_alter_exam_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='ready',
            field=models.BooleanField(default=False),
        ),
    ]
