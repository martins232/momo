# Generated by Django 4.2.7 on 2024-08-27 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_term_unique_term_per_academic_year'),
        ('exam', '0005_studentresult_academic_year_studentresult_subject_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentresult',
            name='grade',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='school.grade'),
            preserve_default=False,
        ),
    ]
