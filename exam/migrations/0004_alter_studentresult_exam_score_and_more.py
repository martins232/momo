# Generated by Django 4.2.7 on 2024-08-24 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_studentresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresult',
            name='exam_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='first_cat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='first_test',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='second_cat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='second_test',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='total_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
