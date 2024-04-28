# Generated by Django 4.2.7 on 2024-04-24 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_student_table'),
        ('teachers', '0003_remove_topic_grade_topic_grade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='grade',
        ),
        migrations.AddField(
            model_name='topic',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.grade'),
        ),
    ]