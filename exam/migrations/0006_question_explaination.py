# Generated by Django 4.2.7 on 2024-06-21 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_remove_exam_unique_exam_alter_exam_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='explaination',
            field=models.CharField(blank=True, null=True),
        ),
    ]
