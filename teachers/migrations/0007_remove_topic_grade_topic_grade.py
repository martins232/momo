# Generated by Django 4.2.7 on 2024-02-20 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('teachers', '0006_topic_grade'),
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
