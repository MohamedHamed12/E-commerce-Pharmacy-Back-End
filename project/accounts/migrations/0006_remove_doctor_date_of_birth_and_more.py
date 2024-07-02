# Generated by Django 4.2.6 on 2024-07-01 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "accounts",
            "0005_alter_customuser_options_alter_customuser_managers_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="doctor",
            name="date_of_birth",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="date_of_birth",
        ),
        migrations.RemoveField(
            model_name="patient",
            name="date_of_birth",
        ),
        migrations.AddField(
            model_name="doctor",
            name="date_birth",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="date_birth",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="patient",
            name="date_birth",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]