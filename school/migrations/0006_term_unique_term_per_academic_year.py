# Generated by Django 4.2.7 on 2024-08-27 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_academicyear_term_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='term',
            constraint=models.UniqueConstraint(fields=('academic_year', 'name'), name='unique_term_per_academic_year'),
        ),
    ]
