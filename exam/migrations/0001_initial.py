# Generated by Django 4.2.7 on 2024-10-25 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('duration', models.DurationField()),
                ('pass_mark', models.FloatField(default=60, verbose_name='Pass mark')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('ready', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('review', models.BooleanField(default=False)),
                ('retake', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(unique=True)),
                ('option_A', models.TextField()),
                ('option_B', models.TextField()),
                ('option_C', models.TextField()),
                ('option_D', models.TextField()),
                ('answer', models.CharField(max_length=250)),
                ('explanation', models.CharField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0.0)),
                ('elapsed_time', models.FloatField(null=True)),
                ('attempts', models.IntegerField(default=0)),
                ('misconduct', models.BooleanField(default=False)),
                ('time_started', models.DateTimeField(null=True)),
                ('time_ended', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField(default=False)),
                ('choices', models.JSONField(default=dict)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.exam')),
            ],
        ),
    ]
