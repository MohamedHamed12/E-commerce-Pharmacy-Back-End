# Generated by Django 4.2.6 on 2024-07-07 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_customuser_deleted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]