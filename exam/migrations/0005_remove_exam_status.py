# Generated by Django 4.2.7 on 2024-02-26 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_alter_question_options_alter_exam_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='status',
        ),
    ]
