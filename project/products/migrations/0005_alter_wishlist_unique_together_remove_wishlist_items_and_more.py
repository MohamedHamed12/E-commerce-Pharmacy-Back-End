# Generated by Django 4.2.6 on 2024-07-04 20:42

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_coupon_discount_type_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wishlist',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='items',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='name',
        ),
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('wishlist', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='products.wishlist')),
            ],
            options={
                'unique_together': {('wishlist', 'product')},
            },
        ),
    ]
