# Generated by Django 5.1.4 on 2024-12-27 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerfeedback',
            name='survey_name',
            field=models.CharField(default=True, max_length=100),
        ),
    ]