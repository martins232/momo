# Generated by Django 4.2.7 on 2024-04-29 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_student_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='request_password',
            field=models.BooleanField(default=False),
        ),
    ]
