# Generated by Django 4.2.7 on 2024-03-02 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_remove_exam_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
