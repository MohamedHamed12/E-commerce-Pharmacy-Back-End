# Generated by Django 4.2.6 on 2024-07-05 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_wishlist_unique_together_remove_wishlist_items_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wishlistitem',
            unique_together=set(),
        ),
    ]
